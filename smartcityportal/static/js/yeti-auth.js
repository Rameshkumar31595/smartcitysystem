/**
 * Refactored GSAP SVG Animation System
 * Stability-first approach: Y-translation only, no rotation/transformOrigin
 * Compatible with mirrored SVG groups (armR uses scale(-1,1))
 */
document.addEventListener("DOMContentLoaded", function () {
  // Defensive wrapper check
  const wrapper = document.querySelector(".yeti-auth-wrapper");
  if (!wrapper) return;

  // Query all required elements within wrapper scope
  const username = wrapper.querySelector("#id_username");
  const password = wrapper.querySelector("#id_password");
  const mySVG = wrapper.querySelector(".mySVG");
  const armL = wrapper.querySelector(".armL");
  const armR = wrapper.querySelector(".armR");
  const eyeL = wrapper.querySelector(".eyeL");
  const eyeR = wrapper.querySelector(".eyeR");
  const mouthSmall = wrapper.querySelector(".mouthSmallBG");
  const mouthMedium = wrapper.querySelector(".mouthMediumBG");
  const mouthLarge = wrapper.querySelector(".mouthLargeBG");

  // Validate critical dependencies
  if (!username || !password || !mySVG || !armL || !armR) return;
  if (!eyeL || !eyeR || typeof TweenMax === "undefined") return;

  /**
   * Initial Arm Position Setup
   * Strategy: Y-translation only, no rotation/transformOrigin
   * Reasoning: Translation is immune to parent transform matrices
   * Values: y=220 (down), visibility=hidden (invisible until needed)
   */
TweenMax.set(armL, {
  x: -93,   // keep this adjustable
  y: 220,
  visibility: "hidden"
});

TweenMax.set(armR, {
  x: -93,   // keep adjustable
  y: 220,
  visibility: "hidden"
});

  /**
   * Mouth State Controller
   * Switches between three mouth expressions based on input length
   */
  function setMouth(type) {
    if (!mouthSmall || !mouthMedium || !mouthLarge) return;
    mouthSmall.style.display = type === "small" ? "" : "none";
    mouthMedium.style.display = type === "medium" ? "" : "none";
    mouthLarge.style.display = type === "large" ? "" : "none";
  }

  // Initialize with small mouth
  setMouth("small");

  /**
   * Eye Tracking System
   * Eyes follow the username input field position
   * Uses bounded translation to prevent extreme eye positions
   */
  function moveEyesToInput(inputEl) {
    const rect = inputEl.getBoundingClientRect();
    const svgRect = mySVG.getBoundingClientRect();

    const inputCenterX = rect.left + rect.width / 2;
    const inputCenterY = rect.top + rect.height / 2;

    const svgCenterX = svgRect.left + svgRect.width / 2;
    const svgCenterY = svgRect.top + svgRect.height / 2;

    // Calculate normalized displacement
    let dx = (inputCenterX - svgCenterX) / 30;
    let dy = (inputCenterY - svgCenterY) / 40;

    // Clamp movement to prevent eyeballs escaping face
    dx = Math.max(-6, Math.min(6, dx));
    dy = Math.max(-5, Math.min(5, dy));

    TweenMax.to([eyeL, eyeR], 0.4, {
      x: dx,
      y: dy,
      ease: Power2.easeOut
    });
  }

  /**
   * Reset Eyes to Center
   * Returns eyes to neutral forward position
   */
  function resetFace() {
    TweenMax.to([eyeL, eyeR], 0.6, {
      x: 0,
      y: 0,
      ease: Power2.easeOut
    });
  }

  /**
   * Arms Cover Eyes Animation
   * Strategy: Symmetric Y-translation only
   * Reasoning: Works reliably with mirrored SVG groups (no rotation conflicts)
   * 
   * Flow:
   * 1. Kill any running arm tweens (prevents animation overlap)
   * 2. Make arms visible
   * 3. Translate both arms to y=25 (up position, covering eyes)
   * 4. Slight delay on armR creates natural sequential motion
   */
  function coverEyes() {
  TweenMax.killTweensOf(armL);
  TweenMax.killTweensOf(armR);

  TweenMax.set(armL, { visibility: "visible" });
  TweenMax.set(armR, { visibility: "visible" });

  TweenMax.to(armL, 0.45, {
    x: -10,
    y: 2,
    ease: Quad.easeOut
  });

  TweenMax.to(armR, 0.45, {
    x: 0,
    y: 2,
    ease: Quad.easeOut,
    delay: 0.1
  });
}

  /**
   * Arms Uncover Eyes Animation
   * Returns arms to resting position and hides them
   * 
   * Flow:
   * 1. Kill any running arm tweens
   * 2. Translate both arms to y=220 (down position)
   * 3. After animation completes, hide arms (visibility=hidden)
   */
  function uncoverEyes() {
  TweenMax.killTweensOf(armL);
  TweenMax.killTweensOf(armR);

  TweenMax.to(armL, 0.6, {
    y: 220,
    ease: Quad.easeOut,
    onComplete: function () {
      TweenMax.set(armL, { visibility: "hidden" });
    }
  });

  TweenMax.to(armR, 0.6, {
    y: 220,
    ease: Quad.easeOut,
    delay: 0.1,
    onComplete: function () {
      TweenMax.set(armR, { visibility: "hidden" });
    }
  });
}
  /**
   * Event Listeners: Username Input Interactions
   * Tracks focus, input changes, and blur events
   */
  username.addEventListener("focus", () => {
    moveEyesToInput(username);
  });

  username.addEventListener("input", () => {
    moveEyesToInput(username);

    // Dynamic mouth expression based on input length
    const len = username.value.length;
    if (len === 0) setMouth("small");
    else if (len < 6) setMouth("medium");
    else setMouth("large");
  });

  username.addEventListener("blur", () => {
    setTimeout(() => {
      resetFace();
      setMouth("small");
    }, 100);
  });

  /**
   * Event Listeners: Password Input Interactions
   * Triggers arm animations for privacy gesture
   */
  password.addEventListener("focus", () => {
    coverEyes();
    setMouth("small");
  });

  password.addEventListener("blur", () => {
    setTimeout(() => {
      uncoverEyes();
      resetFace();
    }, 100);
  });
});