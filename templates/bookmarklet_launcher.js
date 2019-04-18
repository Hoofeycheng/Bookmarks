(function () {
    if(window.bookmarklet !== undefined){
        bookmarklet();
    }else{
        let script = document.createElement('script');
        script.src = 'https://7a876442.ngrok.io/static/js/bookmark.js?r='+ Math.random()*999;
        document.body.appendChild(script);
    }
})();



