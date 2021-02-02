/**
 * HTTP request helpers.
 */

const http = {

  /**
   * @param {string} url
   */
  GET: function GET(url) {
    // Basic GET request in CORS mode;
    // console.(`GET ${url}`);
    return fetch(
      url,
      { mode: 'cors' },
    );
  },

  /**
   * @param {string} url
   * @param {Object} body
   */
  POST: function POST(url, body) {
    // Basic POST request in CORS mode;
    // console.log(`POST ${url} ${JSON.stringify(body)}`);
    return fetch(
      url,
      {
        method: 'POST',
        mode: 'cors',
        headers: {
          'content-type': 'application/json',
        },
        body: JSON.stringify(body),
      },
    );
  },

  summon: function (url, body, output) {
    http.POST(url, body)
    .then(response => {
      console.log('response =', response, Object.keys(response));
      if (!response.ok) response.text().then(text => {throw Error(text)});
      else              return response.json();
    })
    .then(json => {
      console.log(json);
      if (output) {
        document.getElementById(output).innerHTML = json.result;
      }
    })
  }

};
