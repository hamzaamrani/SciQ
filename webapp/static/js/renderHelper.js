function renderHelper() {

    this.convert = function() {
        //
        //  Get the input (it is HTML containing delimited TeX math
        //    and/or MathMLs tags
        //
        var input = document.getElementById("symbolic_expression").value.trim();
        //
        //  Disable the render button until MathJax is done
        //
        //var button = document.getElementById("render");
        //
        //  Clear the old output
        //
        output = document.getElementById('MathOutput');
        output.innerHTML = "`" + input + "`";
        //
        //  Reset the tex labels (and automatic equation numbers, though there aren't any here).
        //  Reset the typesetting system (font caches, etc.)
        //  Typeset the page, using a promise to let us know when that is complete
        //
        MathJax.texReset();
        MathJax.typesetClear();
        MathJax.typesetPromise()
            .catch(function(err) {
                //
                //  If there was an internal error, put the message into the output instead
                //
                output.innerHTML = '';
                output.appendChild(document.createElement('pre')).appendChild(document.createTextNode(err.message));
            })
            .then(function() {
                //
                //  Error or not, re-enable the render button
                //
                //button.disabled = false;
            });
    }
}
var RenderHelper = new renderHelper();