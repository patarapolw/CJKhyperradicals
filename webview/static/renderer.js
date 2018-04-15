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

if(defaultValue.language === 'zh'){
    $('#lang-zh').removeAttr('href');
    $('#lang-ja').attr('href', '#');
} else {
    $('#lang-ja').removeAttr('href');
    $('#lang-zh').attr('href', '#');
}

$("#sentence").keypress(function(event) {
    if (event.which == 13) {
        $('#sentenceSubmit').click();
    }
});

$('#sentenceSubmit').click(function(){
    $.post('/', {
        'sentence': $('#sentence').val()
    }).done(function(content){
        renderChar(content);
    })
})

function renderChar(content){
    content = JSON.parse(content);

    if(!isNaN(parseInt(content.currentChar))){
        $('#character').html('<div class="number">' + content.currentChar + '</div>');
    } else {
        $('#character').text(content.currentChar);
    }

    if(content.charNumber > 0){
        $('#previousChar').removeAttr('disabled');
    } else {
        $('#previousChar').attr('disabled', true);
    }
    if(content.charNumber < content.characters.length-1){
        $('#nextChar').removeAttr('disabled');
    } else {
        $('#nextChar').attr('disabled', true);
    }

    renderCharList('#compositions', content.compositions);
    renderCharList('#supercompositions', content.supercompositions);
    renderCharList('#variants', content.variants);

    $('#vocab').text('');
    if(content.vocab.constructor === [].constructor)
        for(var i=0; i<content.vocab.length; i++){
            $('#vocab').append(
                "<div class='entry'><a href='#' onclick='speak(\"{0}\", \"zh-CN\"); return false;' title='{1}'>{0}</a> {2}</div>"
                .format(content.vocab[i][1], 
                        content.vocab[i][2], 
                        content.vocab[i][3]));
        }
    else {
        for(var i=0; i<content.vocab.data.length; i++){
            $('#vocab').append(
                "<div class='entry'><a href='#' onclick='speak(\"{0}\", \"ja\"); return false;'>{0}</a>（{1}） {2}</div>"
                .format(content.vocab.data[i].japanese[0].word,
                        content.vocab.data[i].japanese[0].reading,
                        content.vocab.data[i].senses[0].english_definitions.join(", ")));
        }
    }

    $('#sentences').text('');
    for(var i=0; i<content.sentences.length; i++){
        var speakerLang = (content.language == 'zh') ? 'zh-CN' : 'ja';
        $('#sentences').append(
            "<div class='entry'><a href='#' onclick='speak(\"{0}\", \"{2}\"); return false;'>{0}</a> {1}</div>"
            .format(content.sentences[i][0],
                    content.sentences[i][1],
                    speakerLang)
        );
    }
}

function speak(vocab, lang){
    $.ajax({
        type: 'POST',
        url: '/speak',
        data: {
            'vocab': vocab,
            'lang': lang
        }
    }).done(function(response){
        if (!(location.hostname === "localhost" || location.hostname === "127.0.0.1"))
        {
            // read base64
            var snd = new Audio("data:audio/x-mp3;base64," + response);
            snd.play();

            // read byteArray
//            var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
//            var source = audioCtx.createBufferSource();
//            audioCtx.decodeAudioData(
//                response,
//                function (buffer) {
//                    source.buffer = buffer;
//                    source.connect(audioCtx.destination);
//                    source.loop = false;
//                });
//            source.start(0);
        }
    })
}

function renderCharList(selector, charList){
    $(selector).text('');
    for(var i=0; i<charList.length; i++){
        var class_name = isNaN(parseInt(charList[i])) ? 'character' : 'number';
        $(selector).append(
            "<div class='{0}' onclick='postChar(\"{1}\")'>{1}</div> ".format(class_name, charList[i]));
    }
}

function previousChar(){
    $.post('/', {
        'charNumber': -1
    }).done(function(content){
        renderChar(content);
    })
}

function nextChar(){
    $.post('/', {
        'charNumber': +1
    }).done(function(content){
        renderChar(content);
    })
}

function postChar(character){
    $.post('/', {
        'character': character
    }).done(function(content){
        renderChar(content);
    })
}

function setLang(lang){
    $.post('/', {
        'language': lang
    }).done(function(content){
        if(lang === 'zh'){
            $('#lang-zh').removeAttr('href');
            $('#lang-ja').attr('href', '#');
        } else {
            $('#lang-ja').removeAttr('href');
            $('#lang-zh').attr('href', '#');
        }
        renderChar(content);
    })
}