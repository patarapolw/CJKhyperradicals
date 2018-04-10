if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) { 
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };
}

document.getElementById("char-number").value = charNumber;
document.getElementById("sentence").value = characters;
document.getElementById("language").value = lang;
if(lang === 'zh'){
    document.getElementById("lang-zh").removeAttribute('href');
} else {
    document.getElementById("lang-ja").removeAttribute('href');
}
setChar();

for(var i=0; i<compositions.length; i++){
    var class_name = isNaN(parseInt(compositions[i])) ? 'character' : 'number';
    document.getElementById("compositions").insertAdjacentHTML('beforeend',
        "<div class='{0}' onclick='loadVocab(\"{1}\")'>{1}</div> ".format(class_name, compositions[i]));
}

for(var i=0; i<supercompositions.length; i++){
    var class_name = isNaN(parseInt(supercompositions[i])) ? 'character' : 'number';
    document.getElementById("supercompositions").insertAdjacentHTML('beforeend',
        "<div class='{0}' onclick='loadVocab(\"{1}\")'>{1}</div> ".format(class_name, supercompositions[i]));
}

for(var i=0; i<variants.length; i++){
    class_name = "character";
    document.getElementById("variants").insertAdjacentHTML('beforeend',
        "<div class='{0}' onclick='loadVocab(\"{1}\")'>{1}</div> ".format(class_name, variants[i]));
}

if(vocab.constructor === [].constructor)
    for(var i=0; i<vocab.length; i++){
        document.getElementById("vocab").insertAdjacentHTML("beforeend",
            "<div><a href='#' onclick='speak(\"{0}\", \"zh-CN\"); return false;' title='{1}'>{0}</a> {2}</div>"
            .format(vocab[i][1], vocab[i][2], vocab[i][3]));
    }
else {
    for(var i=0; i<vocab.data.length; i++){
        document.getElementById("vocab").insertAdjacentHTML("beforeend",
            "<div><a href='#' onclick='speak(\"{0}\", \"ja\"); return false;'>{0}</a>（{1}） {2}</div>"
            .format(vocab.data[i].japanese[0].word,
                    vocab.data[i].japanese[0].reading,
                    vocab.data[i].senses[0].english_definitions.join(", ")));
    }
}

function speak(vocab, lang){
    var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    var source = audioCtx.createBufferSource();
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/speak', true);
    xhr.setRequestHeader('Content-Type', "application/x-www-form-urlencoded; charset=UTF-8");
    xhr.responseType = 'arraybuffer';
    xhr.addEventListener('load', function (r) {
        audioCtx.decodeAudioData(
            xhr.response,
            function (buffer) {
                source.buffer = buffer;
                source.connect(audioCtx.destination);
                source.loop = false;
            });
        source.start(0);
    });
    xhr.send("vocab=" + vocab + "&lang=" + lang);
}

function setChar(){
    if(characters.length > 0 && isNaN(parseInt(characters)))
        document.getElementById("character").innerHTML = characters[charNumber];
    else
        document.getElementById("character").innerHTML = "<div class='number'>" + characters + "</div>"
    document.getElementById("nextChar").disabled = !(charNumber < characters.length - 1);
    document.getElementById("previousChar").disabled = !(charNumber > 0);
}

function previousChar(){
    --document.getElementById("char-number").value;
    document.getElementById("submit-sentence").click();
}

function nextChar(){
    ++document.getElementById("char-number").value;
    document.getElementById("submit-sentence").click();
}

function loadVocab(vocab){
    document.getElementById("sentence").value = vocab;
    document.getElementById("char-number").value = 0;
    document.getElementById("submit-sentence").click();
}

function setLang(lang){
    document.getElementById("language").value = lang;
    document.getElementById("submit-sentence").click();
}