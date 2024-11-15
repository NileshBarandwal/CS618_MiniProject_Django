const SwaggerUIStandalonePreset = {
    name: 'SwaggerUIStandalonePreset',
    layout: 'StandaloneLayout',  // Defines the layout to use

    // Configuration properties for the preset
    defaultModelExpandDepth: 2,
    defaultModelsExpandDepth: 1,
    defaultModelRendering: 'example',
    defaultTryItOutEnabled: true,
};

// Example of how you might define the layout. This should include the structure of the UI.
function StandaloneLayout() {
    // Define how the layout looks and functions here
}

// Export the preset for use in SwaggerUIBundle
window.SwaggerUIStandalonePreset = SwaggerUIStandalonePreset;
