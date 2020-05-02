document.getElementById('hideIntro').onclick = function() {
  document.getElementById('intro').setAttribute('hidden', '')
};

function get_wiki_thumbnail (wikipageid) {
}

function populate() {

}

function load_users () {
  var url = 'api/users/';
  fetch(url,)
    .then(function(response) { return response.json(); })
    .then(function(myJson) { console.log(JSON.stringify(myJson)); })
    .catch(error => conosole.error(error));
}
