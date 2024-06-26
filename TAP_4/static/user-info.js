const template = document.createElement('template');
template.innerHTML = `
    <style>
        .profile {
            padding: 12px;
            border: 1px solid black;
            border-radius: 12px;
            background-color: rgba(128, 255, 255, .5);
            margin-bottom: 12px;
        }
        .profile div {
            margin: 8px;
            font-size: 1.5em;
        }
        .profile p {
            font-size: .9em;
            color: #020202;
        }
    </style>
    <div class="profile">
        <div>
            <slot name="name">
                Default User Name
            </slot>
        </div>
        <p>Email: <slot name="email">defaultusername@exampleemail.com</slot></p>
    </div>
`;

class UserInfoComponent extends HTMLElement {
    static observedAttributes = ["name", "email"];
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.shadowRoot.appendChild(template.content.cloneNode(true));
    }

    updateSlot(attributeName, value) {
        const slot = this.shadowRoot.querySelector(`slot[name="${attributeName}"]`);
        if (slot) {
            slot.textContent = value;
        }
    }

    connectedCallback() {
        this.updateSlot('name', this.getAttribute('name') || 'Default name');
        this.updateSlot('email', this.getAttribute('email') || 'default@example.com');
    }
}

customElements.define("user-info", UserInfoComponent);