let printing =document.querySelector("#printing");
let pdf =document.querySelector("#pdf");
let pop = document.querySelector(".pop");
let cancelx = document.querySelector("#close");
let email_pop = document.querySelector(".email-pop");
let cancel = document.querySelector("#cancel");
let emailing = document.querySelector("#emailing");
element = document.querySelector(".data")
// printing function 
// printing.onclick = ()=>{
//     window.print();
// }

printing.onclick = (element)=>{
    element = document.querySelector(".details")
    var printContent = element.innerHTML;
     var originalContent = window.document.body.innerHTML;
     window.document.body.innerHTML = printContent;
     window.print();
     window.document.body.innerHTML = originalContent;
}

pdf.onclick = ()=>{
    pop.style.display = "block";
}

cancelx.onclick = ()=>{
    pop.style.display = "none";
}
emailing.onclick = ()=>{
    email_pop.style.display = "block";
}

cancel.onclick = ()=>{
    email_pop.style.display = "none";
}


function printMe(element) {
     var printContent = element.innerHTML;
     var originalContent = window.document.body.innerHTML;
     window.document.body.innerHTML = printContent;
     window.print();
     window.document.body.innerHTML = originalContent;
}


