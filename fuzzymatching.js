const overlap = require('talisman/metrics/distance/overlap');
const dice = require('talisman/metrics/distance/dice');
const jaccard = require('talisman/metrics/distance/jaccard');
const normalize = require('talisman/keyers/normalize');

const assert = require('assert');

const createFingerprintTokenizer = require('talisman/tokenizers/fingerprint').createTokenizer;
fingerprint_tokenizer = createFingerprintTokenizer();
const regex_url = /[a-z]\s[A-Z]/

// About arguments
const possibleLang = ["fr", "en", "de"];
const lang = process.argv[2];
if (!possibleLang.includes(lang)) {
  console.log("language must be in ['fr', 'en', 'de']");
  process.exit(1);
}

// Mongo connection
const MongoClient = require('mongodb').MongoClient;

const dbName = 'factiva';
const collection_source_name = 'unfiltered_results_' + lang;
// const collection_target_name = 'filtered_results_' + lang;
const collection_target_name = 'filtered_results_bis_' + lang;

const url = 'mongodb://localhost:27017';

// **Mongo Functions**
const insertResults = function(db, results, callback) {
  const collection = db.collection(collection_target_name);
  try {
    collection.insertOne(results);
  } catch (e) {
    console.log(e)
  }
}


//made to
const deduplicateResults = function(db, callback) {
  const collection = db.collection(collection_source_name);
  const duplicate = collection.aggregate([{
      $group: {
        _id: {
          query: "$query"
        },
        uniqueIds: {
          $addToSet: "$_id"
        },
        count: {
          $sum: 1
        }
      }
    },
    {
      $match: {
        count: {
          "$gt": 1
        }
      }
    }
  ]);
  duplicate.forEach(function(document) {
    const to_be_deleted = new Set();
    for (var i = 0; i < (document.uniqueIds.length - 1); i++) {
      console.log(document.uniqueIds[i])
      to_be_deleted.add(document.uniqueIds[i])
      var myquery = {
        "_id": document.uniqueIds[i]
      };
      try {
        collection.deleteOne({
          "_id": document.uniqueIds[i]
        });
      } catch (e) {
        print(e);
      }
    }
  })
}

const select_result = function(object) {
  query = object.query.split("site:www")[0]
  let best_result = {};
  let score_max = 0;
  if (object.results.length > 0) {
    for (let i = 0; i < object.results.length; i++) {
      if (normalize(object.query) === normalize(object.results[i].title)) {
        best_result = object.results[i];
        best_result.score = 1;
        break;
      }
      query_fp = fingerprint_tokenizer(query);
      result_fp = fingerprint_tokenizer(object.results[i].title);

      url_result_fp = normalize(object.results[i].link)
      regex_url.exec(url_result_fp)
      if (query_fp === result_fp) {
        best_result = object.results[i];
        best_result.score = 1;
        break;
      } else {
        let score_title = overlap(query_fp, result_fp);
        let score_url = overlap(query_fp, url_result_fp);
        let score = Math.max(score_url, score_title)
        if (score > score_max) {
          score_max = score;
          best_result = object.results[i];
        }
      }
    }
  }
  best_result.score = score_max;
  return best_result;
}


MongoClient.connect(url, function(err, client) {
  assert.equal(null, err);
  console.log("Connected successfully to server");

  const db = client.db(dbName);
  const collection_source = db.collection(collection_source_name);
  const collection_target = db.collection(collection_target_name);


  deduplicateResults(db)

  collection_source.find({}).forEach(function(doc) {
    collection_target.findOne({
        "query": doc.query
      })
      .then(result => {
        if (result) {
          console.log("We already assigned a url for this article: ", result);
        } else {
          let best_result = select_result(doc);
          console.log("Searching for : ", doc.query)
          console.log("Found : ", best_result)
          if (best_result.score >= 0.7) { //this is a completely arbitrary threshold

            var response_to_mongo = {
              "query": doc.query,
              "best_result": best_result
            };

            insertResults(db, response_to_mongo, function() {
              collection_target.createIndex({
                query: 1
              }, function(err, result) {
                console.log(result);
              });
            });
          }
        }
      });
  });
  if (!collection_source.find({}).hasNext()) {
    console.log("The job is over")
  }
});
