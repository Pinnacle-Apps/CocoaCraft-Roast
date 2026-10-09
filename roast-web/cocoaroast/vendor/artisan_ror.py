#
# ABOUT
# artisan main canvas
#
# COPYRIGHT (C) 2010-2026 The artisan team represented by
#   Marko Luther <marko.luther@gmx.net> (maintainer) and all contributors
#
# LICENSE
# This program or module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# MAINTAINER
# Marko Luther, 2026
#
# AUTHOR
# Marko Luther, 2023

# Extracted for CocoaCraft Roast; methods below are verbatim from imported Artisan.
# Only the surrounding class and import boundary were added. AGPL-3.0-or-later.
import logging
import warnings
import numpy

_log = logging.getLogger(__name__)


class ArtisanRoR:
    def __init__(self, polyfit: bool = False):
        self.polyfitRoRcalc = polyfit

    @staticmethod # pre condition: 1 < left_index <= len(temp) = len(timex)
    def compute_ror_simple(timex:list[float], temp:list[float], left_index:int, unfiltereddelta:list[float]) -> float:
        timed = timex[-1] - timex[-left_index]   #time difference between last readings
        if temp[-1] != -1 and temp[-left_index] != -1:
            # average the left point of the RoR interval (3 points) without introducing a delay
            if len(temp)>=left_index+2 and 2-left_index<0 and 1-left_index<0 and temp[-left_index-1] != -1 and temp[-left_index + 1] != -1 and temp[-left_index - 2] != -1 and temp[-left_index + 2] != -1:
                return ((temp[-1] - (temp[-left_index - 2] + temp[-left_index - 1] + temp[-left_index] + temp[-left_index + 1] + temp[-left_index + 2])/5.)/timed)*60.  #delta BT (degrees/minute)
            if len(temp)>=left_index+1 and 1-left_index<0 and temp[-left_index-1] != -1 and temp[-left_index + 1] != -1:
                return ((temp[-1] - (temp[-left_index - 1] + temp[-left_index] + temp[-left_index + 1])/3.)/timed)*60.  #delta BT (degrees/minute)
            return ((temp[-1] - temp[-left_index])/timed)*60.  #delta BT (degrees/minute)
        # if any of the readings is -1 we repeat the last RoR reading
        if unfiltereddelta:
            return unfiltereddelta[-1]
        return 0.

    def compute_ror(self, t_final:float, timex:list[float], temp:list[float], unfiltereddelta:list[float], deltaTempSamples:int) -> float:
        # compute RoR
        try:
            if t_final == -1 or len(timex)<2:  # we repeat the last RoR if underlying temperature dropped
                if unfiltereddelta:
                    return unfiltereddelta[-1]
                return 0.
            # normal data received
            #   Delta T = (changeTemp/ChangeTime)*60. =  degrees per minute;
            left_index = min(len(timex),len(temp),max(2, deltaTempSamples + 1))
            # ****** Instead of basing the estimate on the window extremal points,
            #        grab the full set of points and do a formal LS solution to a straight line and use the slope estimate for RoR
            if self.polyfitRoRcalc:
                try:
                    time_vec = timex[-left_index:]
                    temp_samples = temp[-left_index:]
                    with warnings.catch_warnings():
                        warnings.simplefilter('ignore')
                        # using stable polyfit from numpy polyfit module
                        LS_fit = numpy.polynomial.polynomial.polyfit(time_vec, temp_samples, 1)
                        return float(LS_fit[1]*60.)
                except Exception: # pylint: disable=broad-except
                    # a numpy/OpenBLAS polyfit bug can cause polyfit to throw an exception "SVD did not converge in Linear Least Squares" on Windows Windows 10 update 2004
                    # https://github.com/numpy/numpy/issues/16744
                    # we fall back to the two point algo below
                    pass
            return self.compute_ror_simple(timex, temp, left_index, unfiltereddelta)
        except Exception as e: # pylint: disable=broad-except
            _log.exception(e)
            return 0.
