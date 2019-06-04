import "./styles.css";
import * as Phaser from "phaser";
import {
  SingleBullet,
  FrontAndBack,
  Beam,
  Rockets,
  Splitfire,
  OmnidirectionalFire
} from "./weapon";
import { DragonSwarm } from "./enemy";

const config = {
  type: Phaser.WEBGL,
  width: 800,
  height: 600,
  parent: "game",
  physics: {
    default: "arcade",
    impact: {
      setBounds: {
        x: 0,
        y: 0,
        width: 800,
        height: 600,
        thickness: 32
      }
    },
    arcade: {
      setBounds: {
        x: 0,
        y: 0,
        width: 800,
        height: 600,
        thickness: 32
      }
    }
  },
  scene: {
    preload,
    create,
    update,
    extend: {
      player: null,
      cursors: null,
      background: null,
      midground: null,
      midground2: null,
      foreground: null,
      foreground2: null,
      nextFire: 0
    }
  }
};

new Phaser.Game(config);

function preload() {
  this.load.image("background", "/assets/layer8.png");
  this.load.image("midground", "/assets/layer4.png");
  this.load.image("foreground", "/assets/layer3.png");
  this.load.image("player", "/assets/ship.png");
  this.load.bitmapFont(
    "shmupfont",
    "/assets/shmupfont.png",
    "/assets/shmupfont.xml"
  );
  this.load.atlas("dragon", "/assets/dragon.png", "/assets/dragon.json");
  // this.load.spritesheet("dragon", "assets/dragon.png", {
  //   frameWidth: 70,
  //   frameHeight: 50
  // });

  for (let i = 1; i <= 11; ++i) {
    this.load.image(`bullet${i}`, `/assets/bullet${i}.png`);
  }

  this.load.image("jets", "/assets/blue.png");
  this.load.image("flares", "/assets/yellow.png");
}

function create() {
  this.background = this.add.tileSprite(720, 250, 1920, 1080, "background");
  this.background.setScale(0.8, 0.8);

  this.midground = this.add.tileSprite(720, 400, 1920, 1080, "midground");
  this.midground.setScale(0.8, 0.8);
  this.midground2 = this.add.tileSprite(2250, 400, 1920, 1080, "midground");
  this.midground2.setScale(0.8, 0.8);

  this.foreground = this.add.tileSprite(720, 460, 1920, 1080, "foreground");
  this.foreground.setScale(0.8, 0.8);
  this.foreground2 = this.add.tileSprite(2250, 460, 1920, 1080, "foreground");
  this.foreground2.setScale(0.8, 0.8);

  const weapons = CreateWeapons(this);

  this.enemies = CreateEnemies(this);
  CreateDragonAnimations(this);

  this.player = this.physics.add.sprite(64, 200, "player").setDepth(1);
  this.player
    .setDamping(true)
    .setDrag(0.95)
    .setCollideWorldBounds(true)
    .setMaxVelocity(1000)
    .setBounce(0, 0)
    .setImmovable(false);
  this.player.setData({
    health: 5,
    invincible: 1000,
    lastHit: 0,
    weapons,
    selectedWeapon: 0
  });

  this.thrust = this.add.particles("jets").createEmitter({
    x: 1600,
    y: 200,
    angle: { min: 160, max: 200 },
    scale: { start: 0.2, end: 0 },
    blendMode: "ADD",
    lifespan: 600,
    on: false
  });

  this.death = this.add.particles("flares").createEmitter({
    x: 1600,
    y: 200,
    radial: true,
    scale: { start: 0.2, end: 0 },
    blendMode: "ADD",
    lifespan: 1000,
    on: false
  });

  this.cursors = this.input.keyboard.createCursorKeys();
  const enterKey = this.input.keyboard.addKey(
    Phaser.Input.Keyboard.KeyCodes.ENTER
  );
  enterKey.on("up", () => {
    const selectedWeapon = this.player.getData("selectedWeapon");
    const weapons = this.player.getData("weapons");
    const nextWeapon = (selectedWeapon + 1) % weapons.length;
    this.player.setData("selectedWeapon", nextWeapon);
    console.log("setting current weapon to", nextWeapon);
  });
}

function update(time, delta) {
  UpdateBackground.call(this, time, delta);
  UpdatePlayer.call(this, time, delta);

  if (this.player.active) {
    const swarm = this.enemies[
      Phaser.Math.RND.between(0, this.enemies.length - 1)
    ];
    swarm.spawn(time);
  }
  UpdateEnemies.call(this, time, delta);
}

function UpdateBackground(time, delta) {
  this.midground.x -= 0.02 * delta;
  this.midground2.x -= 0.02 * delta;
  this.foreground.x -= 0.03 * delta;
  this.foreground2.x -= 0.03 * delta;

  if (this.midground.x < -800) {
    this.midground.x = 2260;
  }
  if (this.midground2.x < -800) {
    this.midground2.x = 2260;
  }
  if (this.foreground.x < -800) {
    this.foreground.x = 2260;
  }
  if (this.foreground2.x < -800) {
    this.foreground2.x = 2260;
  }
}

function UpdatePlayer(time, delta) {
  this.thrust.setPosition(this.player.x, this.player.y);

  const weapons = this.player.getData("weapons");
  const current = this.player.getData("selectedWeapon");
  const health = this.player.getData("health");

  const currentWeapon = weapons[current];

  if (this.player.isDying && this.player.y >= 590) {
    console.log("player has died");
    this.player.disableBody(true, true);

    this.death.setPosition(this.player.x, this.player.y);
    this.death.setSpeed(50);
    this.death.emitParticle(16);
  }

  if (health <= 0) {
    this.player.setGravityY(1000);
    this.player.isDying = true;
    return;
  }

  const updatePlayerHit = () => {
    const lastHit = this.player.getData("lastHit");
    const invincible = this.player.getData("invincible");

    if (lastHit + invincible < time) {
      this.player.setData("health", health - 1);
      this.player.setData("lastHit", time);
    }
  };

  this.enemies.forEach(swarm => {
    this.physics.collide(this.player, swarm, (player, enemy) => {
      updatePlayerHit();
    });
    this.physics.collide(this.player, swarm.weapon, (player, bullet) => {
      bullet.disableBody(true, true);
      updatePlayerHit();
    });
    this.physics.collide(currentWeapon, swarm, (bullet, enemy) => {
      enemy.isHit = true;
      bullet.disableBody(true, true);
    });
  });

  if (this.player.active) {
    if (this.cursors.left.isDown) {
      this.player.setAccelerationX(-800);
      this.player.flipX = true;
    } else if (this.cursors.right.isDown) {
      this.player.setAccelerationX(800);
      this.player.flipX = false;
    } else {
      this.player.setAccelerationX(0);
    }

    if (this.cursors.up.isDown) {
      this.player.setAccelerationY(-800);
    } else if (this.cursors.down.isDown) {
      this.player.setAccelerationY(800);
    } else {
      this.player.setAccelerationY(0);
    }

    if (Math.abs(this.player.body.velocity.x) > 10) {
      this.thrust.setPosition(
        (this.thrust.x.propertyValue += this.player.flipX ? 16 : -16),
        this.thrust.y.propertyValue
      );
      this.thrust.setSpeed(this.player.body.velocity.x / 2);
      this.thrust.emitParticle(16);
    }

    if (this.cursors.space.isDown && time > this.nextFire) {
      currentWeapon.fire(this.player, time);
    }
  }
}

function UpdateEnemies(time, delta) {}

function CreateWeapons(scene) {
  // let singleShot = new SingleShot(scene);
  //singleShot = scene.impact.add.existing(singleShot);

  const weapons = [
    SingleBullet(scene),
    FrontAndBack(scene),
    Splitfire(scene),
    OmnidirectionalFire(scene),
    Beam(scene),
    Rockets(scene)
  ];

  return weapons;
}

function CreateEnemies(scene) {
  return [DragonSwarm(scene)];
}

function CreateDragonAnimations(scene) {
  var config = {
    key: "dragon_fly",
    frames: scene.anims.generateFrameNames("dragon", {
      prefix: "dragon_1_fly_",
      end: 4,
      zeroPad: 3,
      suffix: ".png"
    }),
    frameRate: 6,
    yoyo: true,
    repeat: -1
  };
  scene.anims.create(config);

  config = {
    key: "dragon_attack",
    frames: scene.anims.generateFrameNames("dragon", {
      prefix: "dragon_1_attack_",
      end: 3,
      zeroPad: 3,
      suffix: ".png"
    }),
    frameRate: 6,
    yoyo: false,
    repeat: 0
  };
  scene.anims.create(config);

  config = {
    key: "dragon_die",
    frames: scene.anims.generateFrameNames("dragon", {
      prefix: "dragon_1_die_",
      end: 5,
      zeroPad: 3,
      suffix: ".png"
    }),
    frameRate: 6,
    yoyo: false,
    repeat: 0
  };
  scene.anims.create(config);

  config = {
    key: "dragon_hit",
    frames: scene.anims.generateFrameNames("dragon", {
      prefix: "dragon_1_hit_",
      end: 2,
      zeroPad: 3,
      suffix: ".png"
    }),
    frameRate: 6,
    yoyo: false,
    repeat: 0
  };
  scene.anims.create(config);
}
