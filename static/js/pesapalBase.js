const pesaPalIframe = document.getElementById('pesaPalIframe');
console.log("Iframe object ", pesaPalIframe);
const pesaPalIframeDiv = document.getElementById('pesaPalIframeDiv');
pesaPalIframe.addEventListener('load', pesaPalIframeLoaded);
const loadingMessage = document.getElementById('loadingMessage')

function pesaPalIframeLoaded() {
    console.log("I frame has loaded")
    pesaPalIframeDiv.classList.remove("d-none");
    pesaPalIframeDiv.classList.add("d-block");
    loadingMessage.classList.remove("d-block");
    loadingMessage.classList.add("d-none");
}