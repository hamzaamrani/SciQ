// Definition of the KEYBOARD
const Keyboard = {
    elements: {
        main: null, // Main keyboard element
        keysContainer: null, // Element that contains all the keys
        keys: [], // Keys
    },

    eventHandlers: {
        oninput: null,
        onclose: null
    },

    properties: {
        value: ""
    },

    object: {
        input_text: null,
        output: null,
        RenderHelper: null
    },

    init() {
        // Create main elements
        this.elements.main = document.createElement("div");
        this.elements.main.setAttribute("id", "keyboard_main");
        this.elements.keysContainer = document.createElement("div");

        // Setup main elements
        this.elements.main.classList.add("keyboard", "keyboard--hidden");
        this.elements.keysContainer.classList.add("keyboard__keys");
        this.elements.keysContainer.appendChild(this._createKeys());

        this.elements.keys = this.elements.keysContainer.querySelectorAll(".keyboard__key");

        // Add to DOM
        this.elements.main.appendChild(this.elements.keysContainer);
        document.body.appendChild(this.elements.main);

        // Automatically use keyboard for elements with .use-keyboard-input
        document.querySelectorAll(".use-keyboard-input").forEach(element => {
            element.addEventListener("focus", () => {
                element.value = this.object.input_text.value
                this.open(element.value, currentValue => {
                    element.value = currentValue;
                    this.object.RenderHelper.convert();
                });
            });
        });
    },

    _createKeys() { // Create HTML FOR EACH ONE OF THE KEYS
        const fragment = document.createDocumentFragment();
        const keyLayout = [
            "π", "°", "∞", "√", "∫", "∑", "∂", "∏", "∀", "∃", "∪", "∩", "∇", "Δ",
            "α", "β", "γ", "ε", "ζ", "η", "θ", "κ", "λ", "μ", "ν", "ξ", "σ", "ρ",
            "τ", "φ", "χ", "ψ", "ω", "Γ", "Θ", "Λ", "Ξ", "ϒ", "Φ", "Ѱ", "Ω",
            "ℵ", "→", "⊕", "⊙", "≠", "≥", "≤", "done"
        ];

        // Creates HTML for an icon
        const createIconHTML = (icon_name) => {
            return `<i class="material-icons">${icon_name}</i>`;
        };

        keyLayout.forEach(key => {
            const keyElement = document.createElement("button");
            const insertLineBreak = ["Δ", "ρ", "Ω", "done"].indexOf(key) !== -1; //when go to newLine creating the keyboard

            // Add attributes/classes
            keyElement.setAttribute("type", "button");
            keyElement.classList.add("keyboard__key");
            keyElement.setAttribute("data-toggle", "tooltip"); // Add attribute for tooltip
            // Switch on key to associate the correct ASCIIMath translation at each keyboard key
            switch (key) {
                case "done":
                    keyElement.classList.add("keyboard__key--dark");
                    keyElement.setAttribute("title", "Done"); // Set title to Done
                    keyElement.innerHTML = createIconHTML("check_circle");
                    keyElement.addEventListener("click", () => {
                        this.close();
                        this._triggerEvent("onclose");
                    });
                    break;

                default:
                    keyElement.textContent = key;
                    keyElement.addEventListener("click", () => {
                        switch (key) {
                            case "∫":
                                key = "int";
                                break;
                            case "π":
                                key = "pi";
                                break;
                            case "σ":
                                key = "sigma";
                                break;
                            case "∞":
                                key = "oo";
                                break;
                            case "√":
                                key = "sqrt"
                                break;
                            case "∑":
                                key = "sum";
                                break;
                            case "∂":
                                key = "partial";
                                break;
                            case "∏":
                                key = "prod";
                                break;
                            case "∀":
                                key = " AA";
                                break;
                            case "∃":
                                key = " EE";
                                break;
                            case "∪":
                                key = "uu";
                                break;
                            case "∩":
                                key = "nn";
                                break;
                            case "∇":
                                key = "grad";
                                break;
                            case "Δ":
                                key = " Delta";
                                break;
                            case "α":
                                key = "alpha";
                                break;
                            case "β":
                                key = "beta";
                                break;
                            case "γ":
                                key = "gamma";
                                break;
                            case "ε":
                                key = "epsilon";
                                break;
                            case "ζ":
                                key = "zeta";
                                break;
                            case "η":
                                key = "eta";
                                break;
                            case "θ":
                                key = "theta";
                                break;
                            case "κ":
                                key = "kappa";
                                break;
                            case "λ":
                                key = "lambda";
                                break;
                            case "μ":
                                key = "mu";
                                break;
                            case "ν":
                                key = "nu";
                                break;
                            case "ξ":
                                key = "xi";
                                break;
                            case "ρ":
                                key = "rho";
                                break;
                            case "τ":
                                key = "tau";
                                break;
                            case "φ":
                                key = "phi";
                                break;
                            case "χ":
                                key = "chi";
                                break;
                            case "ψ":
                                key = "psi";
                                break;
                            case "ω":
                                key = "omega";
                                break;
                            case "Θ":
                                key = " Theta";
                                break;
                            case "Γ":
                                key = " Gamma";
                                break;
                            case "Λ":
                                key = " Lambda";
                                break;
                            case "Ξ":
                                key = " Xi";
                                break;
                            case "ϒ":
                                key = "upsilon";
                                break;
                            case "Φ":
                                key = " Phi";
                                break;
                            case "Ѱ":
                                key = " Psi";
                                break;
                            case "Ω":
                                key = " Omega";
                                break;
                            case "ℵ":
                                key = "aleph";
                                break;
                            case "→":
                                key = "->";
                                break;
                            case "⊕":
                                key = "oplus";
                                break;
                            case "⊙":
                                key = "o.";
                                break;
                            case "≥":
                                key = ">=";
                                break;
                            case "≤":
                                key = "<=";
                                break;

                            default:
                                key = key;
                                break;
                        }
                        this.properties.value += key;
                        this.object.input_text.value = this.properties.value;
                        console.log("Input text = " + this.object.input_text.value);
                        console.log("Keyboard   = " + this.properties.value);
                        this._triggerEvent("oninput");
                    });
                    break;
            }

            fragment.appendChild(keyElement);
            if (insertLineBreak) {
                fragment.appendChild(document.createElement("br"));
            }
        });
        return fragment;
    },

    _triggerEvent(handlerName) { //Trigger oninput or onclose
        console.log("Event triggered! Event name = " + handlerName);
        if (typeof this.eventHandlers[handlerName] == "function") {
            this.eventHandlers[handlerName](this.properties.value);
        }
    },


    open(initialValue, oninput, onclose) {
        console.log("Clicked input!");
        this.properties.value = Keyboard.object.input_text.value;
        this.eventHandlers.oninput = oninput;
        this.eventHandlers.onclose = onclose;

        if (this.elements.main.classList.contains("keyboard--hidden")) {
            console.log("Keyboard was closed");
            this.elements.main.classList.remove("keyboard--hidden");
        } else {
            console.log("Keyboard was open");
            this.close();
            this._triggerEvent("onclose");
        }
    },

    close() {
        console.log("I am in close");
        this.properties.value = " ";
        this.eventHandlers.oninput = oninput;
        this.eventHandlers.onclose = onclose;
        this.elements.main.classList.add("keyboard--hidden");
    }
};

window.addEventListener("DOMContentLoaded", function() {
    Keyboard.init();
    var input_text = document.getElementById('symbolic_expression');
    var output = document.getElementById('MathOutput');
    RenderHelper = new renderHelper();
    Keyboard.object.input_text = input_text;
    Keyboard.object.output = output;
    Keyboard.object.RenderHelper = RenderHelper;

    input_text.addEventListener('keyup', function(event) {
        switch (event.key) {
            case "Backspace":
                Keyboard.properties.value = "";
                Keyboard.properties.value = Keyboard.object.input_text.value;
                Keyboard._triggerEvent("oninput");
                console.log("Pressed backspace");
                console.log("Keyboard value = " + Keyboard.properties.value);
                console.log("Input te value = " + Keyboard.object.input_text.value);
                RenderHelper.convert();
                break;
            case "Spacebar":
                Keyboard.properties.value = "";
                Keyboard.properties.value = Keyboard.object.input_text.value;
                Keyboard._triggerEvent("oninput");
                console.log("Pressed spacebar");
                console.log("Keyboard value = " + Keyboard.properties.value);
                console.log("Input te value = " + Keyboard.object.input_text.value);
                RenderHelper.convert();
                break;
            default:
                if (event.key != "CapsLock" && event.key != "Shift" && event.key != "Tab" && event.key != "Shift" && event.key != "Enter" && event.key != "Control" && event.key != "ArrowUp" && event.key != "ArrowDown" && event.key != "ArrowLeft" && event.key != "ArrowRight" && event.key != "NumLock" && event.key != "F1" && event.key != "F2" && event.key != "F3" && event.key != "F4" && event.key != "F5" && event.key != "F6" && event.key != "F7" && event.key != "F8" && event.key != "F9" && event.key != "F10" && event.key != "F11" && event.key != "F12" && event.key != "Insert") {
                    Keyboard.properties.value = "";
                    Keyboard.properties.value = Keyboard.object.input_text.value;
                    Keyboard._triggerEvent("oninput");
                    console.log("Pressed = " + event.key);
                    console.log("Keyboard value = " + Keyboard.properties.value);
                    console.log("Input te value = " + Keyboard.object.input_text.value);
                    RenderHelper.convert();
                }
                break;
        }
    });
});