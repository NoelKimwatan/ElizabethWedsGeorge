const giftForm = document.getElementById("giftsForm")
const proceedButton = document.getElementById("proceedButton")
const phoneNoInput = document.getElementById("phoneNo")
const pesaPalIframe = document.getElementById("pesaPalIframe")
const loadingMessage = document.getElementById("loadingMessage")

const phoneNoInputInvalid = phoneNoInput.classList.contains("is-invalid");


giftForm.addEventListener("submit", paymentformSubmit);
phoneNoInput.addEventListener("change", phoneInputChange);



function pesaPalIframeLoad() {
    pesaPalIframe.classList.remove("d-none");
    pesaPalIframe.classList.add("d-block");


    loadingMessage.classList.remove("d-block");
    loadingMessage.classList.add("d-none");
}

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


function use_number(node) {
    var empty_val = false;
    const value = node.value;
    if (node.value == '')
        empty_val = true;
    node.type = 'number';
    if (!empty_val)
        node.value = Number(value.replace(/,/g, '')); // or equivalent per locale
}

function use_text(node) {
    var empty_val = false;
    const value = Number(node.value);
    if (node.value == '')
        empty_val = true;
    node.type = 'text';
    if (!empty_val)
        node.value = value.toLocaleString('en');  // or other formatting
}
