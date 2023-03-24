const core = require('@actions/core');
const github = require('@actions/github');
const fs = require('fs');

async function run() {
  try {
    const token = process.env.GITHUB_TOKEN
    console.log(`@ token: ${token}`);
    
    const pull_number = process.env.PULL_NUMBER
    console.log(`@ pull_number: ${pull_number}`);
    
    const octokit = github.getOctokit(token);
    
    const { data: pullRequest } = await octokit.rest.pulls.get({
      owner: github.context.repo.owner,
      repo: github.context.repo.repo,
      pull_number: pull_number
    });
    console.log(`@ pullRequest: ${pullRequest}`);
    
    const files = pullRequest.changed_files;

    let contains_xml = false;
    files.forEach(file => {
      if (file.endsWith(".xml")) {
        contains_xml = true;
        return;
      }
    });

    if (contains_xml) {
      console.log("@ This pull request contains at least one XML file.");
    } else {
      console.log("@ This pull request does not contain any XML files.");
    }
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
