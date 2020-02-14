const se_scraper = require('se-scraper');
const csv = require('csv-parser');
const fse = require('fs-extra');
const assert = require('assert');

// About arguments
const possibleLang = ["fr", "en", "de"];
const lang = process.argv[2];
if(! possibleLang.includes(lang)){
  console.log("language must be in ['fr', 'en', 'de']");
  process.exit(1);
}

// Mongo connection
const MongoClient = require('mongodb').MongoClient;

const dbName = 'factiva';
const collectionName = 'unfiltered_results_old'+lang;
const url = 'mongodb://localhost:27017';
const data = []


// Mongo Functions

const insertResults = function(db, results, callback) {
  const collection = db.collection(collectionName);
  try {
    collection.insertOne(results);
  } catch (e) {
    console.log(e)
  }
}

// Use connect method to connect to the server
MongoClient.connect(url, function(err, client) {
  assert.equal(null, err);
  console.log("Connected successfully to server");

  const db = client.db(dbName);
  const collection = db.collection(collectionName);

  let browserConfig = {
    debug_level: 1,
    output_file: "results/data.json",
    proxy: "http://proxy.medialab.sciences-po.fr:3128",
    random_user_agent: true,
    headless: true,
    use_proxies_only: true,
    apply_evasion_techniques: true
  };

  fse.createReadStream("data_"+lang+"_sorted.csv")
    .pipe(csv())
    .on("data", (row) => data.push(row))
    .on("end", () => {
      (async () => {

        for (var i = 0; i < data.length; i++) {
          const date = new Date(data[i]["date"])
          const datemin = new Date("2015-01-01")

          // if (date > datemin) {
          if (date < datemin) {
            let scrapeJob = {
              search_engine: "bing",
              title: data[i]["title"],
              keywords: [data[i]["title"] + " site:" + data[i]["homepage"]], //actually this is the query
              num_pages: 1,

              //OPTIONAL SETTINGS
              bing_settings: {
                gl: lang, // Determines the Google country to use for the query.
                hl: lang, // Determines the Google UI language to return results.
                start: 0, // Determines the results offset to use
                num: 5, // Determines the number of results to show
              },
              // sleep_range: [2, 4],
              block_assets: true,
              //log_ip_address: true
            };
            console.log(scrapeJob.keywords[0])

            const existingItems = await collection.count({
              query: scrapeJob.keywords[0]
            })

            if (existingItems === 0) {

              var scraper = new se_scraper.ScrapeManager(browserConfig);
              await scraper.start();
              var response = await scraper.scrape(scrapeJob);
              console.dir(response, {
                depth: null,
                colors: true
              });

              //we can't use keys with "." in MongoDB, and we want cleaner data so we clear this way:

              var query = Object.keys(response.results)[0];
              if (query && response.results[query] && response.results[query]["1"]) {
                var response_to_mongo = {
                  "query": query,
                  "results": response.results[query]["1"].results
                };

                insertResults(db, response_to_mongo, function() {
                  collection.createIndex({
                    query: 1
                  }, function(err, result) {
                    console.log(result);
                  });
                });
              } else {
                console.log("There is no response for this query...")
              }
              await scraper.quit();

            }
          } else {
            console.log("This article is too old to be found");
          }

        };
      })();
    });
});
