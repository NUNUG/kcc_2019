import * as Phaser from "phaser";
import { Fireball } from "./weapon";

export class Dragon extends Phaser.Physics.Arcade.Sprite {
  constructor(scene, x, y, key, weapon) {
    super(scene, -500, -500, key);
    this.scaleMode = Phaser.ScaleModes.NEAREST;
    this.born = 0;
    this.lastFired = 0;
    this.fireRate = 2000;
    this.weapon = weapon;
    this.isLeft = true;
    this.isHit = false;

    this.setFlipX(true);
    this.setActive(false);
    this.setVisible(false);
  }

  spawn({ x, y, scale = 1, speed = 400, time }) {
    this.speed = Phaser.Math.GetSpeed(speed, 1);
    this.born = 0;
    this.isDead = false;
    this.isHit = false;

    this.setBounce(0, 0);
    this.setImmovable(false);
    this.enableBody(true, x, y, true, true);

    this.setScale(scale);
    this.anims.play("dragon_fly");
    this.lastFired = time + Phaser.Math.RND.between(300, 1000);
  }

  update(time, delta) {
    let distance = this.speed * delta;

    this.body.velocity.y = 0;

    if (this.isDead) distance /= 4;

    this.x -= distance;
    this.born += delta;

    if (this.isDead) {
      const duration = this.anims.getProgress();
      if (duration === 1) {
        this.disableBody(true, true);
        this.anims.stop();
      }
    }

    if (this.isHit && !this.isDead) {
      // isHit
      this.anims.stop();
      this.anims.play("dragon_die");
      this.isHit = false;
      this.isDead = true;
    }

    if (!this.isDead && time > this.lastFired && this.weapon.fire(this, time)) {
      // isFiring
      this.anims.stop();
      this.anims.play("dragon_attack");
      this.anims.chain("dragon_fly");

      this.lastFired = time + this.fireRate;
    }

    if (this.x < -100 || this.born > 10000) {
      this.disableBody(true, true);
      this.anims.stop();
    }
  }
}

export function DragonSwarm(scene) {
  const weapon = Fireball(scene);

  const swarm = scene.physics.add.group({
    classType: function() {
      return new Dragon(scene, 0, 0, "dragon", weapon);
    },
    key: "dragon",
    runChildUpdate: true,
    maxSize: 64
  });

  swarm.lastSpawned = 0;
  swarm.spawnRate = 500;
  swarm.weapon = weapon;

  swarm.spawn = function DragonSwarmSpawn(time) {
    if (time < this.lastSpawned) return;

    const x = 800;
    const y = Phaser.Math.RND.between(50, 550);

    const dragon = this.get(x, y);
    if (dragon) {
      dragon.spawn({
        x,
        y,
        scale: Phaser.Math.RND.realInRange(0.6, 1.4),
        speed: Phaser.Math.RND.between(100, 400),
        time
      });

      this.lastSpawned = time + this.spawnRate;
    }
  };

  return swarm;
}
