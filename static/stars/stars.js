 document.getElementsByName("rating").forEach(element => element.addEventListener('click',event =>{
        console.log("i m  here new");
        var sim = $("input[name='rating']:checked").val();
        
        $(".myratings").text(sim)

}))