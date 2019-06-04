from pieces import *
import functions

piece_lookup = [
	PieceTypes.LeftL,
	PieceTypes.RightL,
	PieceTypes.LeftS,
	PieceTypes.RightS,
	PieceTypes.Cube,
	PieceTypes.Triad,
	PieceTypes.Bar]

class Piece:
	def __init__(self, game_functions, piece_type, position_colrow, well_size):
		self.piece_type = piece_type
		self.rotation = 0
		self.position = position_colrow
		self.update_matrix()
		self._well_size = well_size
		self.g = game_functions
	def update_matrix(self):
		self.matrix = piece_lookup[self.piece_type][self.rotation]

	def rotate(self, well_matrix):
		old_rotation = self.rotation
		self.rotation = (self.rotation + 1) % 4
		self.update_matrix()
		x, y = self.position
		
		collision_matrix = self.g.copy_matrix(well_matrix)
		self.g.impose_matrix(self.matrix, collision_matrix, self.position)
		has_collided = self.g.has_collisions(collision_matrix)

		if (self.exceeds_right_side(x) or self.exceeds_left_side(x) or has_collided):
			# We moved off the screen or collided with another brick.  Undo the rotation.
			self.rotation = old_rotation
			self.update_matrix()

	def move_down(self):
		x, y = self.position
		y = y + 1
		self.position = (x, y)

	def move_left(self, well_matrix):
		x, y = self.position
		if ((not self.exceeds_left_side(x-1))):
			next_position = (x - 1, y)
			collision_matrix = self.g.copy_matrix(well_matrix)
			self.g.impose_matrix(self.matrix, collision_matrix, next_position)
			will_collide = self.g.has_collisions(collision_matrix)
			if (not will_collide):
				self.position = next_position

	def exceeds_right_side(self, x):
		w, h = self._well_size
		exceeds = False
		col_to_check = (w-1) - x + 1
		if ((col_to_check <= 3) and (col_to_check >= 0)):
			colisempty = self.g.col_is_empty(self.matrix, col_to_check)
			if (not(colisempty)):
				exceeds = True
		return exceeds

	def exceeds_left_side(self, x):
		exceeds = False
		col_to_check = -1 - x
		if ((col_to_check <= 3) and (col_to_check >= 0)):
			colisempty = self.g.col_is_empty(self.matrix, col_to_check)
			if (not(colisempty)):
				exceeds = True
		return exceeds

	def move_right(self, well_matrix):
		x, y = self.position
		if (not self.exceeds_right_side(x + 1)):
			next_position = (x + 1, y)
			collision_matrix = self.g.copy_matrix(well_matrix)
			self.g.impose_matrix(self.matrix, collision_matrix, next_position)
			will_collide = self.g.has_collisions(collision_matrix)
			if (not will_collide):
				self.position = next_position
