import pygame
from pygame.locals import Color, Rect
import random
from graphics import *
import pieces
import piece


random.seed()

class GameFunctions:
	def new_piece(self):
		"""Creates a new piece and places it at the top of the well."""
		piecesCount = len(pieces.PieceTypes.AllPieceTypes)
		next_piece_type = random.randint(0, piecesCount - 1)
		#next_piece_type = 4
		well_cols, _ = self.well_dimensions()
		left_pos = int((well_cols - 4) / 2)
		top_pos = -4
		p = piece.Piece(self, next_piece_type, (left_pos, top_pos), self.well_dimensions())
		# The piece is above the well.
		# Bring the piece down until its bottom row is inside the well.
		if (self.row_is_empty(p.matrix, 3)):
			p.move_down()
			if (self.row_is_empty(p.matrix, 2)):
				p.move_down()
				if (self.row_is_empty(p.matrix, 1)):
					p.move_down()
					if (self.row_is_empty(p.matrix, 0)):
						raise Exception("Piece matrix seems to be empty.")
		return p

	def row_is_empty(self, matrix, rownum):
		"""Determins whether a given row in a piece matrix contains only 0s."""
		for colnum in range(4):
			if (matrix[rownum][colnum] > 0):
				return False
		return True

	def col_is_empty(self, matrix, colnum):
		"""Determines whether a given columnin a piece matrix contains only 0s."""
		for rownum in range(4):
			if (matrix[rownum][colnum] > 0):
				return False
		return True

	def cell_size_in_pixels(self):
		"""Returns the number of pixels in a cell as (width, height)."""
		return (16, 16)

	def well_dimensions(self):
		"""Returns the cellular dimensions of the well."""
		return (10, 20)

	def well_size(self):
		welldw, welldh = self.well_dimensions()
		return (welldw * 16, welldh * 16)

	def well_size_in_pixels(self):
		"""Returns the pixel size of the well as (width, height)."""
		cell_size_x, cell_size_y = self.cell_size_in_pixels()
		well_dim_x, well_dim_y = self.well_dimensions()
		return (cell_size_x * well_dim_x, cell_size_y * well_dim_y)

	def well_pixel_coords(self, screen_size):
		"""Returns the x,y pixel coordinates of the upper-left corner of the well."""
		screen_width, screen_height = screen_size
		well_size_x, well_size_y = self.well_size_in_pixels()
		x = int((screen_width - well_size_x) / 2)
		y = int((screen_height - well_size_y) / 2)
		return (x, y)

	def draw_well_grid(self, screen, screen_size):
		"""This draws a happy little dot in the well at the center of each cell."""
		wellx, welly = self.well_pixel_coords(screen_size)
		cell_width, cell_height = self.cell_size_in_pixels()
		cols, rows = self.well_dimensions()
		for col in range(cols):
			for row in range(rows):
				dot_pos = (wellx + col * cell_width + int(cell_width / 2), welly + row * cell_height + int(cell_height / 2))
				pygame.draw.circle(screen, Color(128, 128, 128, 255), dot_pos, 3)

	def draw_well_matrix(self, screen, screen_size, well_matrix):
		"""This draws the existing set pieces in the well.  It draws a set brick for each cell
		in the well matrix which contains a 1."""
		wellx, welly = self.well_pixel_coords(screen_size)
		cell_width, cell_height = self.cell_size_in_pixels()
		cols, rows = self.well_dimensions()
		for row in range(rows):
			for col in range(cols):
				cell = well_matrix[row][col]
				if (cell >= 1):
					brick_pos = (wellx + col * cell_width, welly + row * cell_height)
					screen.blit(img_well_brick, brick_pos)

	def draw_piece_matrix(self, screen, screen_size, piece):
		"""This draws the current piece on the screen.  It draws a brick for each cell 
		in the piece matrix which contains a 1."""
		posx, posy = piece.position
		for row in range(4):
			for col in range(4):
				cellx, celly = self.cell_position_to_pixels(screen_size, (posx, posy))
				if (GameData.SHOW_MATRIX_SHADOW):
					pygame.draw.line(screen, Color(255, 0, 0, 255), (col * 16 + cellx, row * 16 + celly), ((col+1) * 16 + cellx, (row + 1) * 16 + celly))
				if (posy + row >= 0):
					if (piece.matrix[row][col] == 1):
						screen.blit(img_piece_brick, (col * 16 + cellx, row * 16 + celly))

	def pause_for(self, milliseconds):
		"""Pauses execution for the given time period.  Used for animation sequences and banners."""
		start_ticks = pygame.time.get_ticks()
		while True:
			pygame.time.Clock().tick(1000/30)
			if (pygame.time.get_ticks() > start_ticks + milliseconds):
				break

	def draw_clearings(self, screen, screen_size, well_matrix, crunch_sound):
		"""Draws crunched bricks in each line to be cleared and plays a crunching sound once for each row."""
		wellx, welly = self.well_pixel_coords(screen_size)
		cell_width, cell_height = self.cell_size_in_pixels()
		lines = self.get_lines_to_clear(well_matrix)
		line_count = len(lines)
		ww, wh = self.well_dimensions()
		for line_num in range(line_count):
			for col in range(ww):
				brick_pos = (wellx + col * cell_width, welly + lines[line_num] * cell_height)
				screen.blit(img_crunch_brick, brick_pos)
			pygame.display.update()
			crunch_sound.play()
			self.pause_for(500)

	def draw_well(self, screen, screen_size):
		border_size = 5
		borderx, bordery = self.well_pixel_coords(screen_size)
		borderx = borderx - border_size
		bordery = bordery - border_size
		borderw, borderh = self.well_size_in_pixels()
		borderw = borderw + (2 * border_size)
		borderh = borderh + (2 * border_size)
		pygame.draw.rect(screen, Color(255, 255, 255, 255), Rect(borderx, bordery, borderw, borderh))

		wellx, welly = self.well_pixel_coords(screen_size)
		wellw, wellh = self.well_size_in_pixels()
		pygame.draw.rect(screen, Color(0, 0, 0, 255), Rect(wellx, welly, wellw, wellh))

	def draw_scoreboard(self, screen, screen_size, score):
		"""Draws a box with the score in it onto the screen."""
		screenw, screenh = screen_size
		wellx, welly = self.well_pixel_coords(screen_size)
		wellw, wellh = self.well_size()
		border_size = 5
		padding = 20
		height = 50

		left = wellx + wellw + padding
		right = screenw - padding
		top = welly
		#bottom = top + height
		width = right - left + 1
		
		pygame.draw.rect(screen, Color(255, 255, 255, 255), Rect(left - border_size, top - border_size, width + border_size * 2, height + border_size * 2))
		pygame.draw.rect(screen, Color(0, 0, 0, 255), Rect(left, top, width, height))

		text = str(score)
		font = pygame.font.SysFont("Lucida Console", 32, 1, 0)
		text_surface = font.render(text, False, Color(255, 255, 255, 255))
		screen.blit(text_surface, (left + (width - text_surface.get_width()) / 2, top + (height - text_surface.get_height()) / 2))
		
		

	def compact_well(self, well_matrix):
		"""Bring the contents of the wall down into any recently cleared lines."""
		lines = self.get_lines_to_clear(well_matrix)
		ww, wh = self.well_dimensions()

		# For each cleared line...
		for clear_line_num in lines:
			# Copy each line of the matrix above this one, overwriting the line below it.
			# Don't do it for line 0 because there is no line above it.
			row_num = clear_line_num
			while (row_num >= 1):
				line_above = well_matrix[row_num - 1]
				
				for col_num in range(ww):
					well_matrix[row_num][col_num] = line_above[col_num]
				
				row_num = row_num - 1

		# For line 0, we just clear it explicitly.
		for col_num in range(ww):
			well_matrix[0][col_num] = 0

	def create_empty_matrix(self, rows, cols):
		"""Creates a matrix representing a new empty well."""
		result = []
		for row in range(rows):
			this_row = []
			result.append(this_row)
			for col in range(cols):
				this_row.append(0)
		return result

	def new_well(self):
		"""Creates a matrix representing a new empty well."""
		cols, rows = self.well_dimensions()
		return self.create_empty_matrix(rows, cols)

	def set_piece(self, piece, well_matrix):
		pass

	def copy_matrix(self, source):
		"""Create a duplicate of a matrix.  This is used to create a new piece from the pieces templates."""
		result = []
		for row_num in range(len(source)):
			old_row = source[row_num]
			new_row = []
			for col_num in range(len(old_row)):
				old_cell = old_row[col_num]
				new_row.append(old_cell)
			result.append(new_row)
		return result

	def impose_matrix(self, source, target, source_pos):
		"""writes a matrix onto another matrix at the given cell position.  The result is a matrix addition function.
		So if the same cell in both matrixes contain 1, the output cell will contain 2 (1+1). """

		x_offset, y_offset = source_pos
		source_h = len(source)
		source_w = len(source[0])
		target_h = len(target)
		target_w = len(target[0])
		
		# Copy the target matrix to a temp matrix.
		new_blank_well = self.copy_matrix(target)

		# Impose the piece to the temp matrix
		for source_row_num in range(source_h):
			for source_col_num in range(source_w):
				x, y = (x_offset + source_col_num, y_offset + source_row_num)
				if (x >= 0) and (x <= target_w - 1) and (y >= 0) and (y <= target_h - 1):
					source_cell_value = source[source_row_num][source_col_num]
					target_cell_value = target[y][x]
					new_cell_value = source_cell_value + target_cell_value
					new_blank_well[y][x] = new_cell_value

		# Copy the temp matrix back over the target matrix to send it back out.
		for row_num in range(target_h):
			for col_num in range(target_w):
				target[row_num][col_num] = new_blank_well[row_num][col_num]

	def has_collisions(self, matrix):
		"""Determines if there were any collisions in the result of two merged matrices."""
		matrix_height = len(matrix)
		matrix_width = len(matrix[0])
		for row in range(matrix_height):
			for col in range(matrix_width):
				if (matrix[row][col] > 1):
					return True
		return False

	def line_is_full(self, row):
		"""Indicates if the specified row is completely full of bricks and should be cleared."""
		w = len(row)
		for col in range(w):
			if (row[col] == 0):
				return False
		return True

	def has_lines_to_clear(self, matrix):
		"""Indicates whether any lines are full and need to be cleared."""
		return len(self.get_lines_to_clear(matrix)) > 0

	def get_lines_to_clear(self, matrix):
		"""Returns a list of lines which are full and need to be cleared."""
		result = []
		h = len(matrix)
		for row in range(h):
			if self.line_is_full(matrix[row]):
				result.append(row)
		return result

	def has_hit_bottom(self, piece):
		"""Determines whether the piece has encountered the bottom of the well."""
		x, y = piece.position
		matrix = piece.matrix
		ww, wh = self.well_dimensions()
		wx, wy = (ww - 1, wh - 1)
		result = False
		for rownum in range(4):
			ry = y + rownum
			if (ry >= wy):
				if (not self.row_is_empty(matrix, rownum)):
					result = True
		return result

	def cell_position_to_pixels(self, screen_size, cell_position_colrow):
		"""Convert a cell position within the well to screen x,y coordinates."""
		cell_col, cell_row = cell_position_colrow
		well_pixel_x, well_pixel_y = self.well_pixel_coords(screen_size)
		cell_size_width, cell_size_height = self.cell_size_in_pixels()
		x = well_pixel_x + cell_col * cell_size_width
		y = well_pixel_y + cell_row * cell_size_height
		return (x, y)

	def print_matrix(self, matrix, caption):
		"""Displays the values in the given matrix in the text console.  This is useful for debugging."""
		h = len(matrix)
		w = len(matrix[0])
		print(caption)
		for rownum in range(h):
			print("\t", matrix[rownum])

	def show_game_over(self, screen, screen_size):
		pygame.mixer.music.stop()
		text = "Game Over"
		font = pygame.font.SysFont("Courier New", 32, 1, 0)
		text_surface = font.render(text, False, Color(255, 255, 0, 255))
		surface = pygame.Surface( (text_surface.get_width() + 80, text_surface.get_height() + 80) )
		
		surface.fill(Color(255, 0, 0, 255))

		w, h = screen_size
		screen.blit(surface, ( ((w - surface.get_width()) / 2), ((h - surface.get_height()) / 2) ) )
		screen.blit(text_surface, ( ((w - text_surface.get_width()) / 2), ((h - text_surface.get_height()) / 2) ) )
		pygame.display.update()
		self.pause_for(5000)

	def piece_will_set(self, piece, well_matrix):
		will_set = False
		(x, y) = piece.position
		hit_bottom = self.has_hit_bottom(piece)
		if (hit_bottom):
			will_set = True
		else:
			# Otherwise, if it is going to collide on the next drop, it sets.
			next_position = (x, y + 1)
			collision_matrix = self.copy_matrix(well_matrix)
			self.impose_matrix(piece.matrix, collision_matrix, next_position)
			will_collide = self.has_collisions(collision_matrix)
			if (will_collide):
				will_set = True
		return will_set