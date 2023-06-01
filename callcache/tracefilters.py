import logging
from abc import abstractmethod
from typing import List
from IPython import embed

logger = logging.getLogger(__name__)

class Filter:
    @abstractmethod
    def keep_frame(self, frame):
        '''
        A function that returns true if we should keep the current frame

        Args:
            frame (FrameType): the frame to check

        Returns:
            bool: whether or not the frame should be kept
        '''
        pass

    def __and__(self, other):
        return AndFilter(self, other)

    def __or__(self, other):
        return OrFilter(self, other)

class AndFilter(Filter):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def keep_frame(self, frame):
        return self.left.keep_frame(frame) and self.right.keep_frame(frame)

    def __eq__(self, other):
        if isinstance(other, AndFilter):
            return self.left == other.left and self.right == other.right
        else:
            return False

class OrFilter:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def keep_frame(self, frame):
        return self.left.keep_frame(frame) or self.right.keep_frame(frame)

    def __eq__(self, other):
        if not isinstance(other, OrFilter):
            return False
        else:
            return self.left == other.left and self.right == other.right 

class FunctionNameFilter(Filter):
    '''
    A filter that can be used to filter on function names
    '''
    def __repr__(self):
        return f"FunctionFilter(includes: {self.includes}, excludes: {self.excludes}"

    def __init__(self, include: List = [], exclude: List = []):
        if isinstance(include, str):
            include = [include]
        if isinstance(exclude, str):
            exclude = [exclude]

        logger.debug(f"Creating FunctionFilter: include = {include}, exclude = {exclude}")
        self.includes = include
        self.excludes = exclude

    def keep_frame(self, frame):
        for each in self.includes:
            if frame.f_code.co_name == each:
                logger.debug(f"Keeping frame {frame} because it is in {self.includes}")
                return True 
            
        for each in self.excludes:
            if frame.f_code.co_name == each:
                logger.debug(f"Not keeping frame {frame} because it is in {self.excludes}")
                return False
            
        return False


class FileFilter(Filter):
    def __repr__(self):
        return f"FileFilter(includes: {self.includes}, excludes: {self.excludes})"

    def __init__(self, include: List = [], exclude: List = []):
        if isinstance(include, str):
            include = [include]
        if isinstance(exclude, str):
            exclude = [exclude]
        logger.debug(f"Creating FileFilter: include = {include}, exclude = {exclude}")
        self.includes = include
        self.excludes = exclude

    def keep_frame(self, frame):
        for each in self.includes:
            if frame.f_code.co_filename == each:
                logger.debug(f"Not ignoring frame {frame} because it is in {self.includes}")
                return True 
            
        for each in self.excludes:
            if frame.f_code.co_filename == each:
                logger.debug(f"Ignoring frame {frame} because it is in {self.excludes}")
                return False 
            
        return False