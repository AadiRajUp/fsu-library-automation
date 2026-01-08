
function click_book(id){
    // Dialog or Pop-up for asking email address

    email = prompt("Enter your email address: ");

    if (email == null){
        alert("Email can't be null.");
        return;
    }

    // validatation
    const params = new URLSearchParams( {
        id : id,
        email : email
    });


    window.location.href = `/validation?${params.toString()}`
}


function click_info(id) {
    const url = `http://localhost:5000/info?id=${encodeURIComponent(id)}`;

    fetch(url,{
        method:"GET"
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            alert(
                `SUCESS: ${data.sucess}\n` +
                `NAME: ${data.name}\n` +
                `BOOKED ON : ${data.booked_on}\n`+
                `HOLD : ${data.hold_state}\n` +
                `hold days : ${data.hold_days}\n`
            );
        })
        .catch(error => {
            alert("Error: " + error.message);
        });
}


