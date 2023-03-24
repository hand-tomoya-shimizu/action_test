const core = require('@actions/core');
const fetch = require('node-fetch');

async function run() {
  try {
    const pull_request_url = process.env.GITHUB_PULL_REQUEST_URL;
    const files_url = `${pull_request_url}/files`;
    console.log(`@ files_url: ${files_url}`);

    const response = await fetch(files_url);
    console.log(`@ response: ${response}`);

    const data = await response.json();
    console.log(`@ data: ${data}`);

    const filenames = data.map(file => file.filename);
    const xml_files = filenames.filter(name => name.endsWith('.xml'));

    if (xml_files.length > 0) {
      console.log(`@ XML files detected: ${xml_files.join(', ')}`);
      core.setFailed('XML files are not allowed in this pull request');
    } else {
      console.log('@ No XML files detected');
    }
  } catch (error) {
    core.setFailed(error.message);
  }
}

module.exports = run;
