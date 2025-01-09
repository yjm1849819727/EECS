import lib601.search as search
import lib601.sm as sm

# Indices into the state tuple.
(farmer, goat, wolf, cabbage) = range(4)

class FarmerGoatWolfCabbage(sm.SM):
    startState = ('L', 'L', 'L', 'L')
    legalInputs = ('takeNone', 'takeGoat', 'takeWolf', 'takeCabbage')

    def switch_bank(self, side):
        return 'R' if side == 'L' else 'L'

    def is_bank_safe(self, state, bank, farmer_loc):
        """Check if the specified bank is in a safe state."""
        g, w, c = state[1], state[2], state[3]
        if bank == 'L':
            items_on_bank = [g == 'L', w == 'L', c == 'L']
        else:
            items_on_bank = [g == 'R', w == 'R', c == 'R']
        if farmer_loc != bank:
            # Farmer is not on this bank
            if items_on_bank[0] and items_on_bank[1]:
                # Goat and wolf on bank without farmer
                return False
            if items_on_bank[0] and items_on_bank[2]:
                # Goat and cabbage on bank without farmer
                return False
        return True

    def getNextValues(self, state, action):
        # Current locations
        f_loc, g_loc, w_loc, c_loc = state

        # Determine which item to take
        if action == 'takeNone':
            item = None
        elif action == 'takeGoat':
            item = goat
        elif action == 'takeWolf':
            item = wolf
        elif action == 'takeCabbage':
            item = cabbage
        else:
            return state, state

        # Check if the item to take is on the same side as the farmer
        if item is not None and state[item] != f_loc:
            return state, state

        # Switch farmer's location
        new_f_loc = self.switch_bank(f_loc)

        # Initialize new locations
        new_g_loc, new_w_loc, new_c_loc = g_loc, w_loc, c_loc

        # Move the item if taking one
        if action == 'takeGoat':
            new_g_loc = new_f_loc
        elif action == 'takeWolf':
            new_w_loc = new_f_loc
        elif action == 'takeCabbage':
            new_c_loc = new_f_loc

        new_state = (new_f_loc, new_g_loc, new_w_loc, new_c_loc)

        if not self.is_bank_safe(new_state, 'L', new_f_loc) or not self.is_bank_safe(new_state, 'R', new_f_loc):
            return state, state

        return new_state, new_state

    def done(self, state):
        return state == ('R', 'R', 'R', 'R')


farmerGoatWolfCabbage = FarmerGoatWolfCabbage()


print(search.smSearch(farmerGoatWolfCabbage, initialState=None, goalTest=None, maxNodes=10000, depthFirst=False, DP=True))
