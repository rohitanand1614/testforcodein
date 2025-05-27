function serializeShadowDOM(el, depth = 0) {
    const indent = '  '.repeat(depth);
    let output = '';

    if (!el) return output;

    if (el.nodeType === Node.TEXT_NODE) {
        const text = el.textContent.trim();
        if (text) {
            output += `${indent}#text: "${text}"\n`;
        }
    } else if (el.nodeType === Node.ELEMENT_NODE) {
        output += `${indent}<${el.tagName.toLowerCase()}>\n`;

        if (el.shadowRoot) {
            output += `${indent}  #shadow-root (open)\n`;
            el.shadowRoot.childNodes.forEach(child => {
                output += serializeShadowDOM(child, depth + 2);
            });
        }

        el.childNodes.forEach(child => {
            output += serializeShadowDOM(child, depth + 1);
        });
    }

    return output;
}

// Target the shadow host
const shadowHost = document.querySelector('nsdq-company-profile');
const result = serializeShadowDOM(shadowHost);

// Save as .txt file directly
const blob = new Blob([result], { type: 'text/plain' });
const link = document.createElement('a');
link.href = URL.createObjectURL(blob);
link.download = 'nasdaq-shadow-dom.txt';
document.body.appendChild(link);
link.click();
document.body.removeChild(link);
