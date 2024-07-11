const template = document.createElement('template');
template.innerHTML = `
    <style>
        .profile {
            display: flex;
            flex-direction: column;
            padding: 16px;
            border: 3px solid rgba(128, 68, 0, 0.8);
            background-color: rgba(128, 68, 0, 0.3);
            border-radius: 16px;
        }
        .image-row {
            display: flex;
            flex-direction: row;
            gap: 32px;
            align-items: center;
        }
        .name {
            font-size: 150%;
            font-weight: 500;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .avatar {
            border-radius: 50%;
            aspect-ratio: 1;
            overflow: hidden;
            object-fit: cover;
        }
        .bio {
            display: -webkit-box;
            white-space: pre-wrap;
            -webkit-box-orient: vertical;
            -webkit-line-clamp: 5;
            overflow-y: hidden;
            text-overflow: ellipsis;
        }
    </style>
    <div class="profile">
        <div class="image-row">
            <img id="avatar" class="avatar w-16 sm:w-32">
            
            <div class="name-container">
                <div class="name">
                    <slot name="name">
                        Default User Name
                    </slot>
                </div>

                <div class="title">
                    <slot name="title">
                        Default Title
                    </slot>
                </div>
                
                <div>
                    <span><slot name="email">defaultusername@exampleemail.com</slot></span>
                </div>
            </div>

        </div>

        <div>
            <p id="bio" class="bio"></p>
        </div>
        
    </div>
`;

class UserInfoComponent extends HTMLElement {
    static observedAttributes = ["name", "email", "title", "bio", "avatar"];
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

    updateImageSource(url) {
        const element = this.shadowRoot.getElementById('avatar');
        if (element) {
            element.setAttribute('src', url);
        }
    }

    updateElementInnerHtml(id, html) {
        const element = this.shadowRoot.getElementById(id);
        if (element) {
            element.innerHTML = html;
        }
    }

    connectedCallback() {
        this.updateSlot('name', this.getAttribute('name') || 'Default name');
        this.updateSlot('email', this.getAttribute('email') || 'default@example.com');
        this.updateSlot('title', this.getAttribute('title') || 'Default title');
        this.updateElementInnerHtml('bio', this.getAttribute('bio'));
        this.updateImageSource(this.getAttribute('avatar'));
    }
}

customElements.define("user-info", UserInfoComponent);