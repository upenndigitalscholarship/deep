const build = () => {
    let bB = document.querySelector("#buildButton");
    if (bB.hasAttribute('href')){
        bB.removeAttribute("href")
    }
    bB.text = 'Running Build'
    fetch('/run-build/').then((response) => response.json()).then((data) => bB.text = data.message);
}

let buildButton = document.querySelector("a[href='/run-build/']");
buildButton.setAttribute("id", "buildButton");
buildButton.addEventListener("click", build);