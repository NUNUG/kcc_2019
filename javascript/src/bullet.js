import * as Phaser from "phaser";

export class Bullet extends Phaser.Physics.Arcade.Sprite {
  constructor(scene, x = -50, y = -50, key = "bullet5", baseSpeed = 800) {
    super(scene, x, y, key);
    this.scaleMode = Phaser.ScaleModes.NEAREST;
    this.speed = 0;
    this.born = 0;
    this.angle = 0;
    this.isLeft = false;
    this.baseSpeed = baseSpeed;
  }

  fire({ x = 0, y = 0, velocity = 10, isLeft = false, angle = 0, scale = 1 }) {
    this.speed = Phaser.Math.GetSpeed(
      (isLeft ? -this.baseSpeed : this.baseSpeed) + velocity,
      1
    );
    this.born = 0;
    this.enableBody(true, x, y, true, true);
    this.setAngle(isLeft ? 180 - angle : angle);
    this.isLeft = isLeft;
    this.setScale(scale);
  }

  update(time, delta) {
    const overallVelocity = this.speed * delta;

    // See, Trigonometry is useful!
    let x = overallVelocity * Math.cos(this.rotation);
    let y = overallVelocity * Math.sin(this.rotation);

    this.x += this.isLeft ? -x : x;
    this.y += this.isLeft ? -y : y;
    this.born += delta;

    if (
      this.x <= 0 ||
      this.x >= 800 ||
      this.y <= 0 ||
      this.y >= 600 ||
      this.born > 2000
    ) {
      this.disableBody(true, true);
    }
  }
}
