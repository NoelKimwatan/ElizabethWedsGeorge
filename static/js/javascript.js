const detailsForm = document.getElementById("contribution_form")
const paymentButton = document.getElementById("initiatePayment")


detailsForm.addEventListener("submit", paymentformSubmit);


function paymentformSubmit() {
    console.log("Form was submitted");
    paymentButton.disabled = true;
}