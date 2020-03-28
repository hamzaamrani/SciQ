const Keyboard = {
    elements: {
        main: null, // Main keyboard element
        keysContainer: null, // Element that contains all the keys
        keys: [] // Keys
    },

    eventHandlers: {
        oninput: null,
        onclose: null
    },

    properties: {
        value: ""
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
                this.open(element.value, currentValue => {
                    console.log("Current value = " + currentValue);
                    element.value = currentValue;
                    console.log("element.value = " + element.value);
                });
            });
        });
    },

    _createKeys() { // Create HTML FOR EACH ONE OF THE KEYS
        const fragment = document.createDocumentFragment();
        const keyLayout = [
            "π", "°", "∞", "√", "∫", "∑", "∂", "∏", "∀", "∃", "∪", "∩", "∇", "Δ",
            "α", "β", "γ", "ε", "ζ", "η", "θ", "κ", "λ", "μ", "ν", "ξ", "≠", "ρ",
            "σ", "τ", "φ", "χ", "ψ", "ω", "Γ", "Θ", "Λ", "Ξ", "ϒ", "Φ", "Ѱ", "Ω",
            "℧", "Å", "ℏ", "ℵ", "⇌", "→", "⊕", "⊙", "♂", "♀", "†", "≥", "≤", "done"
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
                    keyElement.textContent = key.toLowerCase();
                    keyElement.addEventListener("click", () => {
                        switch (key) {
                            case "∫":
                                key = "int";
                                break;
                            case "π":
                                key = "pi";
                                break;
                            case "α":
                                key = "alpha";
                                break;
                            case "σ":
                                key = "sigma";
                                break;

                            default:
                                key = key;
                                break;
                        }
                        this.properties.value += key.toLowerCase();
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
        this.properties.value = initialValue || "";
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

    var el = document.getElementById('symbolic_expression');
    el.addEventListener('keydown', function(event) {
        switch (event.key) {
            case "Backspace":
                Keyboard.properties.value = Keyboard.properties.value.substring(0, Keyboard.properties.value.length - 1);
                Keyboard._triggerEvent("oninput");
                console.log(Keyboard.properties.value);
                break;
            case "Spacebar":
                Keyboard.properties.value += " ";
                Keyboard._triggerEvent("oninput");
                console.log(Keyboard.properties.value);
                break;
                /*default:
                    Keyboard.properties.value += event.key;
                    Keyboard._triggerEvent("oninput");
                    console.log("Added = " + event.key);
                    console.log("String is now equals to = " + Keyboard.properties.value);*/
        }
    });

});