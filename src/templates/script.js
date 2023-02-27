addfencer = document.querySelector('#add_fencer');

addfencer.addEventListener("click", (x) => {
    x.preventDefault();
    console.log("sussy")
    let temp = document.querySelector("#fencer_template");
    let clone = temp.content.cloneNode(true);

    clone.querySelector('#name').textContent = "";
    clone.querySelector('#email').textContent = "";

    let form = document.querySelector('#fencer_entry');
    form.appendChild(clone)
});;

