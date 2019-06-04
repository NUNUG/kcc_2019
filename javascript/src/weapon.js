//import * as Phaser from "phaser";
import { Bullet } from "./bullet";

export function SingleBullet(scene) {
  const singleBullet = scene.physics.add.group({
    classType: function() {
      return new Bullet(scene, 0, 0, "bullet5");
    },
    key: "bullet5",
    runChildUpdate: true,
    maxSize: 64
  });

  singleBullet.fireRate = 300;
  singleBullet.lastFired = 0;

  singleBullet.fire = function(source, time) {
    if (time < this.lastFired) return;

    const bullet = this.get(source.x, source.y);

    if (bullet) {
      bullet.speed = 800;
      bullet.born = 0;
      bullet.setActive(true);
      bullet.setVisible(true);
      bullet.fire({
        x: source.x,
        y: source.y,
        velocity: source.body.velocity.x,
        isLeft: source.flipX
      });
      this.lastFired = time + this.fireRate;
    }
  };

  return singleBullet;
}

export function FrontAndBack(scene) {
  const weapon = scene.physics.add.group({
    classType: function() {
      return new Bullet(scene, 0, 0, "bullet5");
    },
    key: "bullet5",
    runChildUpdate: true,
    maxSize: 64
  });

  weapon.fireRate = 400;
  weapon.lastFired = 0;

  weapon.fire = function(source, time) {
    if (time < this.lastFired) return;

    const front = this.get();

    if (front) {
      front.setActive(true);
      front.setVisible(true);
    } else return;

    const back = this.get();

    if (back) {
      back.setActive(true);
      back.setVisible(true);
    } else {
      front.setActive(false);
      front.setVisible(false);
      return;
    }

    front.fire({
      x: source.x,
      y: source.y,
      velocity: source.body.velocity.x,
      isLeft: source.flipX
    });
    back.fire({
      x: source.x,
      y: source.y,
      velocity: source.body.velocity.x,
      isLeft: source.flipX,
      angle: 180
    });

    this.lastFired = time + this.fireRate;
  };

  return weapon;
}

export function Splitfire(scene) {
  const weapon = scene.physics.add.group({
    classType: function() {
      return new Bullet(scene, 0, 0, "bullet5");
    },
    key: "bullet5",
    runChildUpdate: true,
    maxSize: 64
  });

  weapon.fireRate = 500;
  weapon.lastFired = 0;

  weapon.fire = function(source, time) {
    if (time < this.lastFired) return;

    const straight = this.get();

    if (straight) {
      straight.setActive(true);
      straight.setVisible(true);
    } else return;

    const top = this.get();

    if (top) {
      top.setActive(true);
      top.setVisible(true);
    } else {
      straight.setActive(false);
      straight.setVisible(false);
      return;
    }

    const bottom = this.get();

    if (bottom) {
      bottom.setActive(true);
      bottom.setVisible(true);
    } else {
      straight.setActive(false);
      straight.setVisible(false);

      bottom.setActive(false);
      bottom.setVisible(false);
      return;
    }

    straight.fire({
      x: source.x,
      y: source.y,
      velocity: source.body.velocity.x,
      isLeft: source.flipX,
      angle: 0
    });
    top.fire({
      x: source.x,
      y: source.y,
      velocity: source.body.velocity.x,
      isLeft: source.flipX,
      angle: -30
    });
    bottom.fire({
      x: source.x,
      y: source.y,
      velocity: source.body.velocity.x,
      isLeft: source.flipX,
      angle: 30
    });

    this.lastFired = time + this.fireRate;
  };

  return weapon;
}

export function OmnidirectionalFire(scene) {
  const weapon = scene.physics.add.group({
    classType: function() {
      return new Bullet(scene, 0, 0, "bullet5");
    },
    key: "bullet5",
    runChildUpdate: true,
    maxSize: 64
  });

  weapon.fireRate = 800;
  weapon.lastFired = 0;

  weapon.fire = function(source, time) {
    if (time < this.lastFired) return;

    if (this.getTotalFree() < 8) return;

    const bullets = [];
    for (let i = 0; i < 8; ++i) {
      const bullet = this.get();
      bullet.setActive(true);
      bullet.setVisible(true);
      bullets.push(bullet);
    }

    bullets.forEach((bullet, index) => {
      bullet.fire({
        x: source.x,
        y: source.y,
        velocity: source.body.velocity.x,
        isLeft: source.flipX,
        angle: index * 45
      });
    });

    this.lastFired = time + this.fireRate;
  };

  return weapon;
}

export function Beam(scene) {
  const weapon = scene.physics.add.group({
    classType: function() {
      const bullet = new Bullet(scene, 0, 0, "bullet11", 1000);
      return bullet;
    },
    key: "bullet11",
    runChildUpdate: true,
    maxSize: 64
  });

  weapon.fireRate = 45;
  weapon.lastFired = 0;

  weapon.fire = function(source, time) {
    if (time < this.lastFired) return;

    const bullet = this.get(source.x, source.y);

    if (bullet) {
      bullet.setActive(true);
      bullet.setVisible(true);
      bullet.fire({
        x: source.x + (source.flipX ? -40 : 40),
        y: source.y,
        velocity: source.body.velocity.x,
        isLeft: source.flipX
      });
      this.lastFired = time + this.fireRate;
    }
  };

  return weapon;
}

export function Rockets(scene) {
  const weapon = scene.physics.add.group({
    classType: function(s, x, y, k) {
      const bullet = new Bullet(scene, 0, 0, "bullet10", 400);
      return bullet;
    },
    key: "bullet10",
    runChildUpdate: true,
    maxSize: 32
  });

  weapon.fireRate = 600;
  weapon.lastFired = 0;

  weapon.fire = function(source, time) {
    if (time < this.lastFired) return;

    const bullet = this.get();

    if (bullet) {
      bullet.setActive(true);
      bullet.setVisible(true);
      bullet.fire({
        x: source.x,
        y: source.y,
        velocity: source.body.velocity.x,
        isLeft: source.flipX
      });

      this.lastFired = time + this.fireRate;
    }
  };

  return weapon;
}

export function Fireball(scene) {
  const weapon = scene.physics.add.group({
    classType: function(x, s, y, k) {
      const bullet = new Bullet(scene, 0, 0, "bullet8", 600);
      return bullet;
    },
    key: "bullet8",
    runChildUpdate: true,
    maxSize: 64
  });

  weapon.fireRate = 0;
  weapon.lastFired = 0;

  weapon.fire = function(source, time) {
    if (time < this.lastFired) return;

    const bullet = this.get();

    if (bullet) {
      const offsetX = (source.isLeft ? -40 : 40) * source.scaleX;

      bullet.setActive(true);
      bullet.setVisible(true);
      bullet.fire({
        x: source.x + offsetX,
        y: source.y,
        velocity: 0,
        isLeft: source.isLeft,
        scale: source.scaleX
      });

      this.lastFired = time + this.fireRate;
    }

    return !!bullet;
  };

  return weapon;
}
