const assert = require('assert');
const fse = require('fs-extra');
const csv = require('csv-parser');


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
const collection_source_name = 'filtered_results_' + lang + "_copy_bis";
const csv_source = 'article_with_AN_' + lang + '.csv';
const url = 'mongodb://localhost:27017';

// **Mongo Functions**

MongoClient.connect(url, function(err, client) {
  assert.equal(null, err);
  console.log("Connected successfully to server");

  const db = client.db(dbName);
  const collection_source = db.collection(collection_source_name);
  const data = []


  fse.createReadStream(csv_source)
    .pipe(csv())
    .on("data", (row) => data.push(row))
    .on("end", async () => {
      for (let i = 0; i < data.length; i++) {
        let query = data[i]["title"] + " site:" + data[i]["homepage"];
        console.log(query);
        let results = await collection_source.find({
          query: query,
          AN: {
            $exists: false
          }
        });
        let count = await results.count();
        console.log(count);
        if (count > 0) {
          if (count > 1) {
            for (let j = 0; j < count; j++) {
              console.log(results[i]);
            }
          } else {
            console.log("updating", data[i]["AN"]);
            collection_source.updateOne({
                query: query
              }, {
                $set: {
                  AN: data[i]["AN"]
                }
              },
              function(err, res) {
                if (err) throw err;
                console.log(res.result.nModified + " document updated");
              },
            )
          }
        }
      }
      client.close();
    })
})
