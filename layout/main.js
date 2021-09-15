var function_is_running = false;
var PORT = 7306;


// setTimeout(function () {
//     connect_to_socket();
// }, 500);


function connect_to_socket() {
    if (function_is_running) return;

    function_is_running = true;
    let socket = new WebSocket("ws://localhost:" + PORT);
    socket.onopen = function (e) {
        console.log("OPENED");
    };
    socket.onmessage = function (event) {

        console.log(event.data);
        let data = JSON.parse(event.data);
        console.log(`New event | data: ${data}`);
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

// DEBUG
var message = '[{"name": "aa", "score": "3", "color": "#FF0000", "faction": "./factions/GDI.jpg", "background": "./backgrounds/bg1.jpg"}, {"name": "bb", "score": "1", "color": "#1CE11C", "faction": "./factions/GDI.jpg", "background": "./backgrounds/bg1.jpg"}]';
var ndata = JSON.parse(message);
create_players(ndata);

// Goes over players and adds them to the document
function create_players(data) {
    document.getElementById("main").innerHTML = "";
    for (let i = 0; i < data.length; i++)
        create_player(data[i])
}

// Creates a player element and adds it to the document
function create_player(data) {
    let el = `<div class="player">
        <div class="overlay" style="background: ${data['color']}"></div>
        <img class="bg" src="${data['background']}">
        <img class="faction" src="${data['faction']}">
        <div class="ptext name">${data['name']}</div>
        <div class="ptext score">${data['score']}</div>
    </div>`;
    document.getElementById("main").innerHTML += el;
}
