document.addEventListener('DOMContentLoaded', function() {
    const starContainers = document.querySelectorAll('.star-rating');
    
    starContainers.forEach(container => {
        const inputs = container.querySelectorAll('input[type="radio"]');
        const labels = container.querySelectorAll('label');
        
        inputs.forEach((input, index) => {
            input.addEventListener('change', function() {
                if (this.checked) {
                    const value = parseInt(this.value);
                    
                    labels.forEach((label, labelIndex) => {
                        const labelValue = parseInt(inputs[labelIndex].value);
                        if (labelValue <= value) {
                            label.style.color = '#fbbf24';
                        } else {
                            label.style.color = '#ddd';
                        }
                    });
                }
            });
        });
        
        labels.forEach((label, index) => {
            label.addEventListener('mouseenter', function() {
                const value = parseInt(inputs[index].value);
                
                labels.forEach((label, labelIndex) => {
                    const labelValue = parseInt(inputs[labelIndex].value);
                    if (labelValue <= value) {
                        label.style.color = '#fbbf24';
                    } else {
                        label.style.color = '#ddd';
                    }
                });
            });
        });
        
        container.addEventListener('mouseleave', function() {
            const checkedInput = container.querySelector('input[type="radio"]:checked');
            
            if (checkedInput) {
                const value = parseInt(checkedInput.value);
                labels.forEach((label, labelIndex) => {
                    const labelValue = parseInt(inputs[labelIndex].value);
                    if (labelValue <= value) {
                        label.style.color = '#fbbf24';
                    } else {
                        label.style.color = '#ddd';
                    }
                });
            } else {
                labels.forEach(label => {
                    label.style.color = '#ddd';
                });
            }
        });
    });
});
