var function_is_running = false;
var PORT = 7306;

$(document).ready(connect_to_socket);

function connect_to_socket() {
    if (function_is_running) return;

    console.log("Trying to connect...");
    function_is_running = true;
    let socket = new WebSocket("ws://localhost:" + PORT);
    socket.onopen = function (e) {
        console.log("OPENED");
    };
    socket.onmessage = function (event) {
        let data = JSON.parse(event.data);
        console.log(`New event: ${event.data}`);
        create_players(data);
    };

    socket.onclose = function (event) {
        if (event.wasClean) console.log('CLEAN EXIT: ' + event);
        else console.log('UNCLEAN EXIT: ' + event);
        reconnect_to_socket();
    };

    socket.onerror = function (error) {
        console.log('ERROR: ' + error);
        reconnect_to_socket()
    };
}

function reconnect_to_socket(message) {
    console.log('Reconnecting..')
    function_is_running = false;
    setTimeout(function () {
        connect_to_socket();
    }, 500);
}


// Goes over players and adds them to the document
function create_players(data) {
    // Clean main
    $("#main").html("");
    let text_inbetween = `<div id="textouter"><div id="textinner"><span>${data["text"]}</span></div></div>`;
    // Create new players
    for (let i = 0; i < data["player_data"].length; i++) {
        if (i == 0 || data["player_data"][i]["team"] != data["player_data"][i - 1]["team"] || data["player_data"][i]["team"] == "")
            $("#main").append(`<div class='team'><div class='score'><span>${data["player_data"][i]["score"]}</span></div></div>${text_inbetween}`);
        text_inbetween = "";
        create_player(data["player_data"][i]);
    }
    if (data["show_score"]) {
        $(".player").width("90%");
        $(".score").show();
    } else {
        $(".player").width("100%");
        $(".score").hide();
    }
    // Fit text to given width
    $(".name, #textinner").textfill({ maxFontPixels: 2000 });
}

// Creates a player element and adds it to the document
function create_player(data) {
    let el = `<div class="player">
        <div class="overlay" style="background: ${data['color']}"></div>
        <img class="faction" src="${data['faction']}">
        <div class="name"><span>${data['name']}</span></div>
    </div>`;
    $(".team:last").append(el);
}