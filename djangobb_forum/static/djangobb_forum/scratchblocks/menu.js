/* This should be loaded:
 *   - after scratchblocks.js
 *   - after markitup.js
 *   - after scratchblocks._currentLanguage is set
 *   - before markItUp() is run
 *   - before any scratchblocks.parse() calls
 */

// TODO upgrade to v3

// TODO (function($){

function capitalise(text) {
    return text[0].toUpperCase() + text.slice(1);
}

var scratchblocksMenu;
mySettings.markupSet.forEach(function(item) {
    if (item.name === 'Scratchblocks') scratchblocksMenu = item;
});

var code = scratchblocks._currentLanguages.slice().pop();
var language = scratchblocks.allLanguages[code];
function palette(name) {
  if (!language.palette) return name;
  return language.palette[capitalise(name)] || language.palette[name];
}

var blocks = [

  ["forward:", 10],
  ["turnRight:", 15],
  ["turnLeft:", 15],
  "",
  ["heading:", 90],
  ["pointTowards:", ""],
  "",
  ["gotoX:y:"],
  ["gotoSpriteOrMouse:", "mouse-pointer"],
  ["glideSecs:toX:y:elapsed:from:"],
  "",
  ["changeXposBy:", 10],
  ["xpos:", 0],
  ["changeYposBy:", 10],
  ["ypos:", 0],
  "",
  ["bounceOffEdge"],
  "",
  ["setRotationStyle", "left-right"],
  "",
  ["xpos"],
  ["ypos"],
  ["heading"],

  ["say:duration:elapsed:from:", "Hello!", 2],
  ["say:", "Hello!"],
  ["think:duration:elapsed:from:", "Hmm...", 2],
  ["think:", "Hmm..."],
  "",
  ["show"],
  ["hide"],
  "",
  ["lookLike:", "costume1"],
  ["nextCostume"],
  "",
  ["startScene", "backdrop1"],
  ["startSceneAndWait", "backdrop1"],
  ["nextScene"],
  "",
  ["changeGraphicEffect:by:", "color", 25],
  ["setGraphicEffect:to:", "color", 0],
  ["filterReset"],
  "",
  ["changeSizeBy:", 10],
  ["setSizeTo:", 100],
  "",
  ["comeToFront"],
  ["goBackByLayers:", 1],
  "",
  ["costumeIndex"],
  ["scale"],
  "",
  ["sceneName"],
  ["backgroundIndex"],

  ["playSound:", "pop"],
  ["doPlaySoundAndWait", "pop"],
  ["stopAllSounds"],
  "",
  ["playDrum", 1, 0.25],
  ["rest:elapsed:from:", 0.25],
  "",
  ["noteOn:duration:elapsed:from:", 60, 0.5],
  ["instrument:", 1],
  "",
  ["changeVolumeBy:", -10],
  ["setVolumeTo:", 100],
  ["volume"],
  "",
  ["changeTempoBy:", 20],
  ["setTempoTo:", 60],
  ["tempo"],

  ["clearPenTrails"],
  "",
  ["stampCostume"],
  "",
  ["putPenDown"],
  ["putPenUp"],
  "",
  ["penColor:"],
  ["changePenHueBy:"],
  ["setPenHueTo:", 0],
  "",
  ["changePenShadeBy:"],
  ["setPenShadeTo:", 50],
  "",
  ["changePenSizeBy:", 1],
  ["penSize:", 1],

  ["whenGreenFlag"],
  ["whenKeyPressed", "space"],
  ["whenClicked"],
  ["whenSceneStarts", "backdrop1"],
  "",
  ["whenSensorGreaterThan", "loudness", 10],
  "",
  ["whenIReceive", ""],
  ["broadcast:", ""],
  ["doBroadcastAndWait", ""],

  ["wait:elapsed:from:", 1],
  "",
  ["doRepeat", 10],
  ["doForever"],
  "",
  ["doIf"],
  ["doIfElse", false, [], []],
  ["doWaitUntil"],
  ["doUntil"],
  "",
  ["stopScripts", "all"],
  "",
  ["whenCloned"],
  ["createCloneOf"],
  ["deleteClone"],

  ["touching:", ""],
  ["touchingColor:"],
  ["color:sees:"],
  ["distanceTo:", ""],
  "",
  ["doAsk", "What's your name?"],
  ["answer"],
  "",
  ["keyPressed:", "space"],
  ["mousePressed"],
  ["mouseX"],
  ["mouseY"],
  "",
  ["soundLevel"],
  "",
  ["senseVideoMotion", "motion", "Stage"],
  ["setVideoState", "on"],
  ["setVideoTransparency", 50],
  "",
  ["timer"],
  ["timerReset"],
  "",
  ["getAttribute:of:", "x position", "Sprite1"],
  "",
  ["timeAndDate", "minute"],
  ["timestamp"],
  ["getUserName"],

  ["+", "", ""],
  ["-", "", ""],
  ["*", "", ""],
  ["/", "", ""],
  ["-"],
  ["randomFrom:to:", 1, 10],
  ["-"],
  ["<", "", ""],
  ["=", "", ""],
  [">", "", ""],
  "",
  ["&"],
  ["|"],
  ["not"],
  "",
  ["concatenate:with:", "hello ", "world"],
  ["letter:of:", 1, "world"],
  ["stringLength:", "world"],
  "",
  ["%", "", ""],
  ["rounded", ""],
  "",
  ["computeFunction:of:", "sqrt", 9],

  ["readVariable", "foo"],
  "",
  ["setVar:to:"],
  ["changeVar:by:"],
  "",
  ["showVariable:"],
  ["hideVariable:"],

  ["contentsOfList:", "list"],
  "",
  ["append:toList:", "thing", "list"],
  "",
  ["deleteLine:ofList:", 1, "list"],
  ["insert:at:ofList:", "thing", 1, "list"],
  ["setLine:ofList:to:", 1, "list", "thing"],
  "",
  ["getLine:ofList:", 1, "list"],
  ["lineCountOfList:", "list"],
  ["list:contains:", "list", "thing"],
  "",
  ["showList:", "list"],
  ["hideList:", "list"],

];

var foo = "";
var el = document.createElement('div');

var currentCategory = null;
var currentSubMenu = null;

blocks.forEach(function(array) {
  if (array === "") {
    foo += "\n";
    return;
  }

  var block = scratchblocks.Block.fromJSON(language, array);

  for (var i=0; i<block.children.length; i++) {
    var child = block.children[i];
    if (child.isInput && !child.isColor) {
      block.children[i] = new scratchblocks.Input(child.shape, "...");
      break;
    } else if (child.isScript) {
      debugger;
      block.children[i] = scratchblocks.parse("...").scripts[0];
      break;
    }
  }

  var output = block.stringify();

  var category = block.info.category;
  if (currentCategory != category) {
      foo += '\n// ' + category + '\n\n';
      currentCategory = category;
      currentSubMenu = {name: palette(category) + ' :: ' + category,
                        dropMenu: []};
      scratchblocksMenu.dropMenu.push(currentSubMenu);
  }

  foo += '\n' + output;

  var display = output;
  if (block.info.selector === 'computeFunction:of:') {
    display = "([... v] of (9) :: operators)";
  }
  el.textContent = display;
  currentSubMenu.dropMenu.push({
    name: el.innerHTML,
    replaceWith: output,
    //openWith: output.slice(0, splitIndex),
    //closeWith: output.slice(splitIndex + offset)
  });
  //foo += output.slice(0, splitIndex) + output.slice(splitIndex + offset) + '\n';
});

var doneBlockText = [];

[].forEach(function(spec) {
  return;

    var text = spec[0],
        shape = shape_ids[spec[1]],
        category = category_ids[spec[2]],
        defaults = spec.slice(3);

    if (doneBlockText.indexOf(text) > -1) return;
    doneBlockText.push(text);


    var info = scratchblocks.blocksBySelector[text];
    if (info.flag && info.flag !== 'cstart') return;

    var args = [];
    var pat = /%(.)(?:\.[A-z]+)?/g;
    var match;
    while (match = pat.exec(text)) {
        args.push(spec_shapes[match[1]]);
        if (args.length > 1 && match[1] == 'c') {
            args[0] = '[#00ff00]';
            args[1] = '[#0000ff]';
        }
    }
    defaults[0] = '...';
    args = args.map(function(item) {
        var fallback = (item[0] === '(') ? '0' : ' ';
        return item.replace('_', defaults.shift() || fallback);
    });

    var output = language.blocks[blockid] || blockid;
    if (blockid.indexOf('@') > -1) {
        for (otherid in language.aliases) {
            if (language.aliases[otherid] === blockid) {
                output = otherid;
            }
        }
    }


    var preview = '';
    output = output.replace(/_/g, ' _ ').replace(/ +/g, ' ').trim();
    if (blockid === '_ of _' || blockid === 'length of _') {
        preview = ' :: ' + category;
    } else if ((scratchblocks2.find_block(output, []) || {}).category !== category) {
        output += ' :: ' + category;
    }

    while (args.length) {
        output = output.replace('_', args.shift());
    }

    if (currentCategory != category) {
        foo += '\n// ' + category + '\n\n';
        currentCategory = category;

        name = palette(category);
        currentSubMenu = {name: name + ' :: ' + category,
                          dropMenu: []};
        scratchblocksMenu.dropMenu.push(currentSubMenu);

        if (category === 'variables') {
            currentSubMenu.dropMenu.push({
                name:'(variable)',
                openWith:'(',
                // placeHolder: 'variable',
                closeWith:')',
            });
        } else if (category === 'list') {
            currentSubMenu.dropMenu.push({
                name:'(list :: list)',
                openWith:'(',
                // placeHolder: 'list',
                closeWith:' :: list)',
            });
        }
    }

    var preview = output.replace('<...>', '<>') + preview;

    if (shape) {
        output = shape.replace('_', output);
        preview = shape.replace('_', preview);
    }

    if (info.flag === 'cstart') output += '\n    |\nend\n';
    if (info.shape === 'hat') output = '\n' + output;

    preview = preview.replace(/&/g, '&amp;')
                     .replace(/</g, '&lt;')
                     .replace(/>/g, '&gt;');

    // Put the cursor at the first input if possible,
    // otherwise the first C mouth,
    // otherwise at the end.
    var splitIndex = output.indexOf('...');
    var offset = 3;
    if (splitIndex === -1) {
        splitIndex = output.indexOf('|');
        offset = 1;
    } else {
        output = output.replace('|', '');
    }
    if (splitIndex > -1) {
        currentSubMenu.dropMenu.push({
            name: preview,
            openWith: output.slice(0, splitIndex),
            closeWith: output.slice(splitIndex + offset)
        });
        foo += output.slice(0, splitIndex) + output.slice(splitIndex + offset) + '\n';
    } else {
        currentSubMenu.dropMenu.push({
            name: preview,
            replaceWith: output,
        });
        foo += output + '\n';
    }

});

// TODO this whole thing stinks. Just rewrite scratchblocks to use proper block specs!

scratchblocksMenu.dropMenu.push({
    name: palette('More Blocks') + ' :: custom',
    dropMenu: [
        {name: language.define, openWith: language.define + ' '},
        {name: '(input :: custom-arg)', openWith: '(', closeWith: ')'},
    ],
});

scratchblocksMenu.dropMenu.push({
    name: (palette('Tips') || 'Help') + ' :: grey',
    beforeInsert: function () {
        window.location = 'http://wiki.scratch.mit.edu/wiki/Block_Plugin/ForumHelp';
    },
});


mySettings.beforeInsert = function(h) {
    h.originalSelection = h.selection;
};

mySettings.afterInsert = function(h) {
    if (!(h.hasOwnProperty('openWith') || h.hasOwnProperty('replaceWith'))
        || $.inArray(h.name, [
            'Bold', 'Italic', 'Underline', 'Stroke', 'Picture', 'Link',
            'Size', 'Big', 'Small', 'Bulleted list', 'Numeric list',
            'List item', 'Quotes', 'Smiles', 'Smile', 'Neutral', 'Sad',
            'Big smile', 'Yikes', 'Wink', 'Hmm', 'Tongue', 'Lol', 'Mad',
            'Roll', 'Cool', 'Clean', 'Preview',
            'Paste browser / operating system versions']) > -1) {
        return;
    }


    var contents = $(h.textarea).attr('value'),
        cursor,
        originalCursor,
        lineStartCursor,
        OPEN_BRACKETS = "<([",
        CLOSE_BRACKETS = "])>";


    if('selectionStart' in h.textarea) {
        cursor = h.textarea.selectionStart;
    } else if('selection' in document) {
        h.textarea.focus();
        var sel = document.selection.createRange();
        var selLength = document.selection.createRange().text.length;
        sel.moveStart('character', -h.textarea.value.length);
        cursor = sel.text.length - selLength;
    }
    originalCursor = cursor;

    // Are we inserting inside a line?
    if (h.caretPosition > 0 && contents.charAt(h.caretPosition - 1) !== "\n") {
        var inserted = h.replaceWith || (h.openWith + (h.closeWith || ""));
        var open = h.replaceWith || h.openWith;

        if (h.originalSelection) {
            // Consume surrounding brackets.
            var testIndex = h.caretPosition,
                endIndex = testIndex + inserted.length + h.originalSelection.length;
            var charBefore = contents.charAt(testIndex - 1),
                charAfter = contents.charAt(endIndex);
            if (OPEN_BRACKETS.indexOf(charBefore) > -1 && CLOSE_BRACKETS.indexOf(charAfter) > -1) {
                contents = (contents.slice(0, testIndex - 1) +
                            contents.slice(testIndex, endIndex) +
                            contents.slice(endIndex + 1));
                originalCursor -= 1;
            }
        } else {
            contents = contents.slice(0, h.caretPosition) + contents.slice(h.caretPosition + inserted.length);

            if (contents.charAt(h.caretPosition) === "\n" && !contents.charAt(h.caretPosition - 1) === "\n") {
                // At end of line. Insert newline
                contents = contents.slice(0, h.caretPosition) + '\n' + inserted + contents.slice(h.caretPosition);
                h.caretPosition += 1;
                originalCursor += 1;
            } else {
                // Inside line. Remove block and add on a new line.
                if (OPEN_BRACKETS.indexOf(inserted.charAt(0)) === -1) { // stack block
                    // Look for newline
                    var eol = h.caretPosition;
                    while (contents.charAt(eol) !== "\n" && eol <= contents.length) {
                        eol += 1;
                    }

                    contents = contents.slice(0, eol) + '\n' + inserted + contents.slice(eol);
                    originalCursor = eol + open.length + 1;

                } else { // reporter block
                    // Consume surrounding brackets.
                    var testIndex = h.caretPosition;
                    var charBefore = contents.charAt(testIndex - 1),
                        charAfter = contents.charAt(testIndex);
                    if (OPEN_BRACKETS.indexOf(charBefore) > -1 && CLOSE_BRACKETS.indexOf(charAfter) > -1) {
                        contents = contents.slice(0, testIndex - 1) + contents.slice(testIndex + 1);
                        testIndex -= 1;
                        originalCursor -= 1;
                    }

                    contents = contents.slice(0, testIndex) + inserted + contents.slice(testIndex);
                }
            }
        }
    }

    // Look for scratchblocks tag
    cursor -= 15;
    while (!/\[\/?scratchblocks\]/.test(contents.slice(cursor, originalCursor)) && cursor >= 0) {
        cursor -= 1;
    }

    // Insert scratchblocks tag if needed
    if (!/\[scratchblocks\]/.test(contents.slice(cursor, originalCursor))) {
        contents = contents.slice(0, h.caretPosition) + '[scratchblocks]\n' + contents.slice(h.caretPosition);
        contents += '\n[/scratchblocks]';
        originalCursor += 16;
    }

    $(h.textarea).attr('value', contents);

    if (h.textarea.setSelectionRange) {
        h.textarea.focus();
        h.textarea.setSelectionRange(originalCursor, originalCursor);
    } else if (h.textarea.createTextRange) {
        var range = h.textarea.createTextRange();
        range.collapse(true);
        range.moveEnd('character', originalCursor);
        range.moveStart('character', originalCursor);
        range.select();
    }
};
