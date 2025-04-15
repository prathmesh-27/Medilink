document.addEventListener('DOMContentLoaded', function () {
    // Get all hotspots
    const hotspots = document.querySelectorAll('.hotspot');
    const infoPanel = document.getElementById('info-panel');
    const partTitle = document.getElementById('part-title');
    const partContent = document.getElementById('part-content');

    // Body part information database
    const bodyPartInfo = {
        'head': {
            title: 'Head',
            content: `
                <p>The head contains the brain, which is the control center of the body. It processes sensory information, controls movement, and regulates bodily functions.</p>
                <p>Key components include:</p>
                <ul>
                    <li>Brain: Controls thoughts, memory, and bodily functions</li>
                    <li>Eyes: Organs of vision</li>
                    <li>Ears: Organs of hearing and balance</li>
                    <li>Nose: Organ of smell</li>
                    <li>Mouth: For eating, speaking, and breathing</li>
                </ul>
                <p>Common conditions: Headaches, migraines, concussions, and stroke.</p>
            `
        },
        'chest': {
            title: 'Chest',
            content: `
                <p>The chest (thorax) contains vital organs including the heart and lungs, protected by the ribcage.</p>
                <p>Key components include:</p>
                <ul>
                    <li>Heart: Pumps blood throughout the body</li>
                    <li>Lungs: Responsible for respiration</li>
                    <li>Ribcage: Protects vital organs</li>
                    <li>Esophagus: Tube connecting mouth to stomach</li>
                </ul>
                <p>Common conditions: Heart disease, pneumonia, bronchitis, and asthma.</p>
            `
        },
        'abdomen': {
            title: 'Abdomen',
            content: `
                <p>The abdomen contains the digestive organs and other vital structures.</p>
                <p>Key components include:</p>
                <ul>
                    <li>Stomach: Digests food</li>
                    <li>Liver: Detoxifies and produces proteins</li>
                    <li>Pancreas: Produces digestive enzymes and insulin</li>
                    <li>Intestines: Absorb nutrients and eliminate waste</li>
                    <li>Kidneys: Filter blood and produce urine</li>
                </ul>
                <p>Common conditions: Appendicitis, gallstones, irritable bowel syndrome, and ulcers.</p>
            `
        },
        'right-arm': {
            title: 'Right Arm',
            content: `
                <p>The arm is a limb attached to the shoulder, used for movement and manipulation of objects.</p>
                <p>Key components include:</p>
                <ul>
                    <li>Humerus: Upper arm bone</li>
                    <li>Radius and Ulna: Lower arm bones</li>
                    <li>Biceps and Triceps: Major arm muscles</li>
                    <li>Elbow: Joint connecting upper and lower arm</li>
                    <li>Hand: For grasping and fine motor skills</li>
                </ul>
                <p>Common conditions: Tennis elbow, carpal tunnel syndrome, and fractures.</p>
            `
        },
        'left-arm': {
            title: 'Left Arm',
            content: `
                <p>The arm is a limb attached to the shoulder, used for movement and manipulation of objects.</p>
                <p>Key components include:</p>
                <ul>
                    <li>Humerus: Upper arm bone</li>
                    <li>Radius and Ulna: Lower arm bones</li>
                    <li>Biceps and Triceps: Major arm muscles</li>
                    <li>Elbow: Joint connecting upper and lower arm</li>
                    <li>Hand: For grasping and fine motor skills</li>
                </ul>
                <p>Common conditions: Tennis elbow, carpal tunnel syndrome, and fractures.</p>
            `
        },
        'right-leg': {
            title: 'Right Leg',
            content: `
                <p>The leg is a limb used for standing, walking, and running.</p>
                <p>Key components include:</p>
                <ul>
                    <li>Femur: Thigh bone</li>
                    <li>Tibia and Fibula: Lower leg bones</li>
                    <li>Patella: Kneecap</li>
                    <li>Quadriceps and Hamstrings: Major leg muscles</li>
                    <li>Foot: For balance and movement</li>
                </ul>
                <p>Common conditions: Knee injuries, shin splints, and ankle sprains.</p>
            `
        },
        'left-leg': {
            title: 'Left Leg',
            content: `
                <p>The leg is a limb used for standing, walking, and running.</p>
                <p>Key components include:</p>
                <ul>
                    <li>Femur: Thigh bone</li>
                    <li>Tibia and Fibula: Lower leg bones</li>
                    <li>Patella: Kneecap</li>
                    <li>Quadriceps and Hamstrings: Major leg muscles</li>
                    <li>Foot: For balance and movement</li>
                </ul>
                <p>Common conditions: Knee injuries, shin splints, and ankle sprains.</p>
            `
        }
    };

    // Add click event listeners to all hotspots
    hotspots.forEach(hotspot => {
        hotspot.addEventListener('click', function () {
            // Remove active class from all hotspots
            hotspots.forEach(h => h.classList.remove('active'));

            // Add active class to clicked hotspot
            this.classList.add('active');

            // Get the body part data attribute
            const bodyPart = this.getAttribute('data-part');

            // Update the info panel with the corresponding information
            if (bodyPartInfo[bodyPart]) {
                partTitle.textContent = bodyPartInfo[bodyPart].title;
                partContent.innerHTML = bodyPartInfo[bodyPart].content;

                // Add animation to the info panel
                infoPanel.style.animation = 'none';
                setTimeout(() => {
                    infoPanel.style.animation = 'fadeIn 0.5s ease-in-out';
                }, 10);
            }
        });
    });

    // Add hover effect to make the experience more interactive
    document.querySelectorAll('.hotspot').forEach(hotspot => {
        hotspot.addEventListener('mouseenter', function () {
            this.querySelector('.hotspot-dot').style.transform = 'scale(1.2)';
        });

        hotspot.addEventListener('mouseleave', function () {
            this.querySelector('.hotspot-dot').style.transform = 'scale(1)';
        });
    });

    // Add keyboard navigation for accessibility
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Tab') {
            // Add focus styles
            document.activeElement.classList.add('keyboard-focus');
        }
    });
});