# coding: utf8
# Part of the bioread package for reading BIOPAC data.
#
# Copyright (c) 2010 Board of Regents of the University of Wisconsin System
#
# Written by John Ollinger <ollinger@wisc.edu> and Nate Vack <njvack@wisc.edu>
# at the Waisman Laboratory for Brain Imaging and Behavior, University of
# Wisconsin-Madison

import numpy as np


class Datafile(object):
    """
    A data file for the AcqKnowledge system. Generally, gonna be created
    from a file by readers.AcqReader.
    """

    def __init__(self,
            graph_header=None, channel_headers=None, foreign_header=None,
            channel_dtype_headers=None, samples_per_second=None, name=None):
        self.graph_header = graph_header
        self.channel_headers = channel_headers
        self.foreign_header = foreign_header
        self.channel_dtype_headers = channel_dtype_headers
        self.samples_per_second = samples_per_second
        self.name = name
        self.channels = None
        self.__named_channels = None

    @property
    def named_channels(self):
        if self.__named_channels is None and self.channels is not None:
            self.__named_channels = {}
            for c in self.channels:
                self.__named_channels[c.name] = c

        return self.__named_channels


class Channel(object):
    """
    An individual channel of Biopac data. Has methods to access raw data from
    the file, as well as a scaled copy if the raw data is in integer format.
    Also generally created by readers.AcqReader.
    """

    def __init__(self,
        freq_divider=None, raw_scale_factor=None, raw_offset=None,
        raw_data=None, name=None, units=None, fmt_str=None,
        samples_per_second=None):

        self.freq_divider = freq_divider
        self.raw_scale_factor = raw_scale_factor
        self.raw_offset = raw_offset
        self.name = name
        self.units = units
        self.fmt_str = fmt_str
        self.samples_per_second = samples_per_second
        self.__raw_data = raw_data
        self.__data = None
        self.__upsampled_data = None

    @property
    def raw_data(self):
        """
        The raw data recorded in the AcqKnowledge file. For channels stored
        as floats, these are the values reported in the AcqKnowledge interface;
        for ints, the values need to be scaled -- see data().
        """
        return self.__raw_data

    @property
    def data(self):
        """
        The channel's data, scaled by the raw_scale_factor and offset. These
        will be the values reported by AcqKnowledge.
        """
        if self.__data is None:
            self.__data = (self.raw_data*self.raw_scale_factor)+self.raw_offset
        return self.__data

    @property
    def upsampled_data(self):
        """
        The channel's data, sampled at the native frequency of the file.
        All channels should have the same number of points using this method.
        Nearest-neighbor sampling is used.
        """
        if self.__upsampled_data is None:
            total_samples = self.data.shape[0]*self.freq_divider
            self.__upsampled_data = self.data[
                np.arange(total_samples)//self.freq_divider]
        return self.__upsampled_data
