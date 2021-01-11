from flask import Flask
from flask import jsonify
from github import Github

app = Flask(__name__)
g = Github("6bdb81ff0791e0d49d655e39f6d9eee35cd5e790")


@app.route('/repos/<owner>/<repo>/pulls/<int:pull_number>')
def get_specify_pull(owner, repo, pull_number):
    repo = g.get_repo("{}/{}".format(owner, repo))
    pr = repo.get_pull(pull_number)
    return jsonify(pr.raw_data)


@app.route('/repos/<owner>/<repo>/pulls/approved/latest')
def get_latest_approved_issue(owner, repo):
    repo = "{}/{}".format(owner, repo)
    q = "repo:{} is:pr review:approved".format(repo)
    issues = g.search_issues(q, sort="updated", order="desc")
    r = {}
    for issue in issues:
        r = issue
        break
    return jsonify(r.raw_data)


@app.route('/repos/<owner>/<repo>/contributors')
def get_repo_contributors(owner, repo):
    repo = g.get_repo("{}/{}".format(owner, repo))
    contributors = repo.get_contributors()
    result = []
    for contributor in contributors:
        result.append(contributor.raw_data)
    return jsonify(result)


@app.route('/repos/<owner>/<repo>/contributor/<contributor_name>')
def get_repo_specify_contributor(owner, repo, contributor_name):
    repo = g.get_repo("{}/{}".format(owner, repo))
    contributors = repo.get_contributors()
    r = {}
    for contributor in contributors:
        if contributor.name == contributor_name or contributor.login == contributor_name:
            r = contributor.raw_data
            break
    return jsonify(r)


if __name__ == "__main__":
    app.run(host='localhost', port=7099 ,debug=True)