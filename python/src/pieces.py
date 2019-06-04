class PieceTypes:
	LeftL = [
		[
			[ 1, 1, 0, 0],
			[ 0, 1, 0, 0],
			[ 0, 1, 0, 0],
			[ 0, 0, 0, 0]
		],
		[
			[ 0, 0, 1, 0],
			[ 1, 1, 1, 0],
			[ 0, 0, 0, 0],
			[ 0, 0, 0, 0]
		],
		[
			[ 1, 0, 0, 0],
			[ 1, 0, 0, 0],
			[ 1, 1, 0, 0],
			[ 0, 0, 0, 0]
		],
		[
			[ 1, 1, 1, 0],
			[ 1, 0, 0, 0],
			[ 0, 0, 0, 0],
			[ 0, 0, 0, 0]
		]
	]

	RightL = [
		[
			[ 1, 1, 0, 0],
			[ 1, 0, 0, 0],
			[ 1, 0, 0, 0],
			[ 0, 0, 0, 0]
		],
		[
			[ 1, 1, 1, 0],
			[ 0, 0, 1, 0],
			[ 0, 0, 0, 0],
			[ 0, 0, 0, 0]
		],
		[
			[ 0, 1, 0, 0],
			[ 0, 1, 0, 0],
			[ 1, 1, 0, 0],
			[ 0, 0, 0, 0]
		],
		[
			[ 1, 0, 0, 0],
			[ 1, 1, 1, 0],
			[ 0, 0, 0, 0],
			[ 0, 0, 0, 0]
		]
	]

	LeftS = [
		[
			[ 0, 1, 1, 0],
			[ 1, 1, 0, 0],
			[ 0, 0, 0, 0],
			[ 0, 0, 0, 0]
		],
		[
			[ 1, 0, 0, 0],
			[ 1, 1, 0, 0],
			[ 0, 1, 0, 0],
			[ 0, 0, 0, 0]
		],
		[
			[ 0, 1, 1, 0],
			[ 1, 1, 0, 0],
			[ 0, 0, 0, 0],
			[ 0, 0, 0, 0]
		],
		[
			[ 1, 0, 0, 0],
			[ 1, 1, 0, 0],
			[ 0, 1, 0, 0],
			[ 0, 0, 0, 0]
		]
	]

	RightS = [
		[
			[ 1, 1, 0, 0],
			[ 0, 1, 1, 0],
			[ 0, 0, 0, 0],
			[ 0, 0, 0, 0]
		],
		[
			[ 0, 1, 0, 0],
			[ 1, 1, 0, 0],
			[ 1, 0, 0, 0],
			[ 0, 0, 0, 0]
		],
		[
			[ 1, 1, 0, 0],
			[ 0, 1, 1, 0],
			[ 0, 0, 0, 0],
			[ 0, 0, 0, 0]
		],
		[
			[ 0, 1, 0, 0],
			[ 1, 1, 0, 0],
			[ 1, 0, 0, 0],
			[ 0, 0, 0, 0]
		]
	]

	Cube = [
		[
			[ 1, 1, 0, 0],
			[ 1, 1, 0, 0],
			[ 0, 0, 0, 0],
			[ 0, 0, 0, 0]
		],
		[
			[ 1, 1, 0, 0],
			[ 1, 1, 0, 0],
			[ 0, 0, 0, 0],
			[ 0, 0, 0, 0]
		],
		[
			[ 1, 1, 0, 0],
			[ 1, 1, 0, 0],
			[ 0, 0, 0, 0],
			[ 0, 0, 0, 0]
		],
		[
			[ 1, 1, 0, 0],
			[ 1, 1, 0, 0],
			[ 0, 0, 0, 0],
			[ 0, 0, 0, 0]
		]
	]

	Triad = [
		[
			[ 0, 1, 0, 0],
			[ 1, 1, 1, 0],
			[ 0, 0, 0, 0],
			[ 0, 0, 0, 0]
		],
		[
			[ 1, 0, 0, 0],
			[ 1, 1, 0, 0],
			[ 1, 0, 0, 0],
			[ 0, 0, 0, 0]
		],
		[
			[ 1, 1, 1, 0],
			[ 0, 1, 0, 0],
			[ 0, 0, 0, 0],
			[ 0, 0, 0, 0]
		],
		[
			[ 0, 1, 0, 0],
			[ 1, 1, 0, 0],
			[ 0, 1, 0, 0],
			[ 0, 0, 0, 0]
		]
	]

	Bar = [
		[
			[ 0, 1, 0, 0],
			[ 0, 1, 0, 0],
			[ 0, 1, 0, 0],
			[ 0, 1, 0, 0]
		],
		[
			[ 0, 0, 0, 0],
			[ 1, 1, 1, 1],
			[ 0, 0, 0, 0],
			[ 0, 0, 0, 0]
		],
		[
			[ 0, 1, 0, 0],
			[ 0, 1, 0, 0],
			[ 0, 1, 0, 0],
			[ 0, 1, 0, 0]
		],
		[
			[ 0, 0, 0, 0],
			[ 1, 1, 1, 1],
			[ 0, 0, 0, 0],
			[ 0, 0, 0, 0]
		]
	]
	AllPieceTypes = [LeftL, RightL, LeftS, RightS, Cube, Triad, Bar]