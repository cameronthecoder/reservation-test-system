const form = document.getElementById('form');
const room_id = document.getElementById('room');
const end_date = document.getElementById('end_date');
const start_date = document.getElementById('start_date');

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

form.addEventListener('submit', e => {
    e.preventDefault();

    fetch(window.location, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            'start_date': start_date.value,
            'end_date': end_date.value,
            'room_id': room_id.value
        })
    }).then(resp => {
        return resp.json();
    }).then(data => {
        console.log(data);
    })
})