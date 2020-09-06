var stripe = Stripe(stripe_test_key);
const form = document.getElementById('form');
const start_date = document.getElementById('start_date');
const end_date = document.getElementById('end_date');
const first_name = document.getElementById('first_name');
const last_name = document.getElementById('last_name');
const room = document.getElementById('room');
const button = document.getElementById('reserve-button');


form.addEventListener('submit', function(e) {
    e.preventDefault();
    button.classList.add('is-loading');
    fetch('/create-session', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'room_id': room.value,
            'first_name': first_name.value,
            'last_name': last_name.value,
            'start_date': start_date.value,
            'end_date': end_date.value,
        })
    }).then(function(r) {
        console.log(r);
        return r.json();
    }).then(function(resp) {
        const sessionId = resp.id;
        stripe.redirectToCheckout({
            sessionId: sessionId
        });
    });
});

const configure_start_date = () => {
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+1; //January is 0!
    var yyyy = today.getFullYear();
    if(dd < 10){
        dd = '0' + dd
    } 
    if(mm < 10){
        mm = '0' + mm;
    } 
    today = yyyy+'-'+mm+'-'+dd;
    start_date.setAttribute("min", today);
};
configure_start_date();