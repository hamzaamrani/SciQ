const Keyboard = {
    elements: {
        main: null,
        keysContainer: null,
        keys: []
    },

    eventHandlers: {
        onInput: null,
        onClose: null
    },

    properties: {
        value: ""
    },


    init() {
        // Create main elements
        this.elements.main = document.createElement("div");
        this.elements.keysContainer = document.createElement("div");

        //setUp main elements
        this.elements.main.classList.add("keyboard", "keyboard--hidden");
        this.elements.keysContainer.classList.add("keyboard_keys");
        this.elements.keysContainer.appendChild(this._createKeys());

        // Add to DOM
        this.elements.main.appendChild(this.elements.keysContainer);
        document.body.appendChild(this.elements.main);


        // Automatically use keyboard for elements 
        document.querySelectorAll(".use-keyboard-input").forEach(element => {
            element.addEventListener("focus", () => {
                this.open(element.value, currentValue => {
                    element.value = currentValue;
                })
            });
        });

    },


    _createKeys() {
        const fragment = document.createDocumentFragment();
        const keyLayout = [
            "π", "°", "∞", "√", "∫", "∑", "∂", "∏", "∀", "∃", "∪", "∩", "∇", "Δ",
            "α", "β", "γ", "ε", "ζ", "η", "θ", "κ", "λ", "μ", "ν", "ξ", "≠", "ρ",
            "σ", "τ", "φ", "χ", "ψ", "ω", "Γ", "Θ", "Λ", "Ξ", "ϒ", "Φ", "Ѱ", "Ω",
            "℧", "Å", "ℏ", "ℵ", "⇌", "→", "⊕", "⊙", "♂", "♀", "†", "≥", "≤", "done"
        ];

        // Create the html for icons
        const createIconHTML = (icon_name) => {
            return '<i class="material-icons"> check_circle</i>';
        };

        keyLayout.forEach(key => {
            const keyElement = document.createElement("button");
            const insertLineBreak = ["Δ", "ρ", "Ω", "done"].indexOf(key) !== -1; //when go to newLine creating the keyboard

            // Add attributes/classes
            keyElement.setAttribute("type", "button");
            keyElement.classList.add("keyboard_key");

            switch (key) {
                case "done":
                    keyElement.classList.add("keyboard_key--wide", "keyboard_key--dark")
                    keyElement.innerHTML = createIconHTML('check_circle');
                    keyElement.addEventListener("click", () => {
                        this.close(this.onInput, this.onClose); //closing the keyboard
                        this._triggerEvent("onClose");
                    });
                    break;

                default:
                    keyElement.textContent = key.toLowerCase();

                    keyElement.addEventListener("click", () => {
                        this.properties.value += key.toLowerCase();
                        this._triggerEvent("onInput");
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

    _triggerEvent(handlerName) {
        if (typeof this.eventHandlers[handlerName] == "function") {
            this.eventHandlers[handlerName](this.properties.value);
        }
    },

    open(initialValue, onInput, onClose) {
        this.properties.value = initialValue || "";
        this.eventHandlers.onInput = onInput;
        this.eventHandlers.onClose = onClose;
        this.elements.main.classList.remove("keyboard--hidden");
    },

    close(onInput, onClose) {
        this.properties.value = "";
        this.eventHandlers.onInput = onInput;
        this.eventHandlers.onClose = onClose;
        this.elements.main.classList.add("keyboard--hidden");

    }


};

window.addEventListener("DOMContentLoaded", function() {
    Keyboard.init();
    /*Keyboard.open("dcode", function(currentValue) {
        console.log("Value changed! here it is : " + currentValue);
    }, function(currentValue) {
        console.log("keyboard closed! Finishing value: " + currentValue);
    });*/
});