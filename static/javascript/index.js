
function click_book(id){
    // Check available or not : TODO
    // Dialog or Pop-up for asking email address

    email = prompt("Enter your email address: ");

    if (email == null){
        alert("Email can't be null.");
        return;
    }

    // validatation
    const validateUrl = "/validation";
    const params = new URLSearchParams( {
        id : id,
        email : email
    });


    window.location.href = `/validation?${params.toString()}`
}