/* Scratchblocks Backpack plugin
* -----------------------------
* 
* Use the Scratch Backpack API to create 'add to backpack' buttons! In the
* words of Dora the Explorer,
*
*   I'm the Backpack loaded up    /  With things and knick-knacks too!
*   Anything that you might need  /  I got inside for you!
*   Backpack, Backpack!
*   Backpack, Backpack!
*   Yeah!
*
* This plugin is MIT-licensed.
*
* -- Kartik, spring 2016
*/
~function(scratchblocks) {
  // This is the API-level heavy lifting. When I say "API", I mean "what I
  // glean from poking around cookies and tcpdump output", so, well, here's
  // hoping the ST doesn't change anything anytime soon.

  function addObjectToBackpack(obj, yes, no) {
    // We're going to regex against the cookie because that's the One Best Way
    // To Do It(tm).
    var CSRFTOKEN = document.cookie?
            (document.cookie.match(/csrftoken=(.*?);/) ?
             document.cookie.match(/csrftoken=(.*?);/)[1] :
             null) :
            null;
    var USER = window.Scratch && window.Scratch.INIT_DATA.LOGGED_IN_USER.model?
           window.Scratch.INIT_DATA.LOGGED_IN_USER.model.username :
           null;
    if (!(CSRFTOKEN && USER)) {
      return no('Not logged in.');
    }
    var x = new XMLHttpRequest();
    x.open(
      "GET",
      "//scratch.mit.edu/internalapi/backpack/"+USER+"/get/",
      true
    );
    x.onerror = no;
    x.onload = function() {
      var current_backpack = x.responseText;
      var parsed = JSON.parse(current_backpack);
      parsed.push(obj);
      var new_backpack = JSON.stringify(parsed);

      var y = new XMLHttpRequest();
      y.open(
        "POST",
        "//scratch.mit.edu/internalapi/backpack/"+USER+"/set/",
        true
      );
      y.setRequestHeader("X-CSRFToken", CSRFTOKEN);
      y.onload = function() {
        if (y.responseText === "true") {
          // we are happy campers
          yes();
        } else {
          // we are not happy campers
          no(y.responseText);
        }
      }
      y.onerror = no;
      y.send(new_backpack); // whoosh!
    }
    x.send();
  }
  function addScriptToBackpack(name, scripts, yes, no) {
    if (!yes) { yes = function(x) {console.log(x)}; }
    if (!no ) { no  = function(x) {console.log(x)}; }
    addObjectToBackpack(
      {"type": "script", "name": name, "scripts": scripts},
      yes,
      no
    );
  }

  var backpackButton = function(parsed) {
    var node = document.createElement('button');
    var scripts = parsed.toJSON(); // we pretend to trust this output
    scripts = scripts.scripts.map(function(x) {return x[2];});
    node.addEventListener('click', function() {
      node.textContent = "Working...";
      addScriptToBackpack(
        window.prompt( // aha! a legitimate use for window.prompt!
            "Title",
            'Exported from '+document.title.replace(' - Discuss Scratch', '')
        ),
        scripts,
        function() {
          node.textContent = "Added!";
          // look at me using semantic properties for great good!
          node.disabled = 'disabled';
        },
        function(e) {
          node.textContent = "Error: "+e;
          node.disabled = 'disabled';
        }
      );
    }, false);
    node.textContent = "Add to backpack";
    node.className   = "backpackButton";
    return node;
  };
  scratchblocks.backpackButton = backpackButton;
}(window.scratchblocks); // Try your best to install to `scratchblocks`...
