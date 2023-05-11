const giftForm = document.getElementById("giftsForm")
const proceedButton = document.getElementById("proceedButton")
const phoneNoInput = document.getElementById("phoneNo")

const phoneNoInputInvalid = phoneNoInput.classList.contains("is-invalid");


giftForm.addEventListener("submit", paymentformSubmit);
phoneNoInput.addEventListener("change", phoneInputChange)


function phoneInputChange() {
    const phoneNo = document.getElementById("phoneNo").value
    const phoneNoLength = phoneNo.length

    console.log("Phone number length ", phoneNoLength)

    if (phoneNoLength >= 9 && phoneNoLength <= 12) {
        phoneNoInput.classList.remove("is-invalid");
        phoneNoInput.classList.add("is-valid");
    } else {
        phoneNoInput.classList.add("is-invalid");
        phoneNoInput.classList.remove("is-valid");
    }
}

function paymentformSubmit(event) {
    event.preventDefault()
    console.log("Form was submitted");

    if (phoneNoInput.classList.contains("is-invalid")) {
        console.log("Form is invalid")
    } else {
        //Submit successfull
        console.log("Form is valid")
        proceedButton.disabled = true;
        giftForm.submit();
    }


}