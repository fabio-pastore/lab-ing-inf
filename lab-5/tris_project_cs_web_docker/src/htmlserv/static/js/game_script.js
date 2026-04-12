let table = null;
let container = null;

function addListeners() {
    for (let row of table) {
        for (let cell of row) {
            cell.addEventListener("click", async (e) => {
                let curr_cell = e.target;
                if (curr_cell && curr_cell.innerText === '' && !(checkGameEnded())) {
                    switchCells(true); // turn cells events off temporarily to wait for CPU to play (not very elegant but it works...)
                    let cell_id = curr_cell.id;
                    let cell_r = cell_id[0];
                    let cell_c = cell_id[1];
                    let form_data = new URLSearchParams();
                    let response = null;

                    form_data.append('row', cell_r);
                    form_data.append('col', cell_c);

                    try {
                        response = await fetch('/mark_board', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded',
                            },
                            body: form_data
                        });
                    }

                    catch (err) {console.error("Could not send form to server: ", err);}

                    console.info(`[INFO] Successfully sent mark request for cell @ coords (${cell_r}, ${cell_c}) to server.`)

                    let html_string = await response.text();
                    document.documentElement.innerHTML = html_string; // update page
                    init();
                    switchCells(true); // turn cell events off after page update
                    if (checkGameEnded()) return;

                    await new Promise(r => setTimeout(r, 250)); // wait 250ms

                    // send new POST for CPU's turn
                    form_data = new URLSearchParams();
                    form_data.append('row', -1)
                    form_data.append('col', -1) // arbitrary values that won't be used by mark() in html_server.py

                    try {
                        response = await fetch('/mark_board', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded',
                            },
                            body: form_data
                        });
                    }

                    catch (err) {console.error("Could not send form to server: ", err);}
                    
                    console.info(`[INFO] Successfully sent mark request for CPU turn to server.`)

                    html_string = await response.text();
                    document.documentElement.innerHTML = html_string; // update page
                    init(); // this automatically turns event back on since we are resetting the page to default
                    switchCells(false) // although you can never be too sure...
                }
                
            });
        }
    }
}

function switchCells(off) {
    if (off) {container.classList.add('disabled');}
    else {container.classList.remove('disabled');}
}

function init() {

    table = [
    [document.getElementById("00"), document.getElementById("01"), document.getElementById("02")],
    [document.getElementById("10"), document.getElementById("11"), document.getElementById("12")],
    [document.getElementById("20"), document.getElementById("21"), document.getElementById("22")]
    ];

    container = document.querySelector('.container');

    addListeners();
    updatePlayAgain();
}

function updatePlayAgain() {
    const pa = document.getElementById("restart");
    const res = document.getElementById("res");
    if (res.innerText != '') {
        pa.style.display = "inline-block";
    }
}

function checkGameEnded() {
    const res = document.getElementById("res");
    return (res.innerText != '');
}

init();