#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Ringtail results manager
#

from .mpmanager import MPManager
from .exceptions import ResultsProcessingError
from .storagemanager import StorageManager, StorageManagerSQLite
import typing
import logging


class ResultsManager:
    def __init__(
        self,
        storageman: StorageManager,
        storageman_class = StorageManagerSQLite,
        parser_manager: str = "multiprocessing",
        mode: str = "dlg",
        chunk_size: int = 1, # what is this
        max_poses: int = 3,
        interaction_tolerance: float = None,
        store_all_poses: bool = False,
        add_interactions: bool = False,
        interaction_cutoffs: list = [3.7, 4.0],
        file_sources: dict = {
            "file": [[]],
            "file_path": {"path": [[]], "pattern": "*.dlg*", "recursive": None},
            "file_list": [[]],
            "receptor_file": None,
            "target": None,
        },
        max_proc: int = None,
    ):
        self.parser_manager = parser_manager ### set to default
        self.mode = mode
        self.chunk_size = chunk_size ### set to default
        self.max_poses = max_poses
        self.store_all_poses = store_all_poses
        self.interaction_tolerance = interaction_tolerance
        self.target = file_sources["target"]
        self.add_interactions = add_interactions
        self.interaction_cutoffs = interaction_cutoffs
        self.receptor_file = file_sources["receptor_file"] 
        self.file_sources = file_sources
        self.file_pattern = file_sources["file_path"]["pattern"]
        self.max_proc = max_proc
        self.storageman_class = storageman_class
        self.storageman = storageman

    def process_results(self):
        # check that we have file source(s)
        if (
            self.file_sources["file"] == [[]]
            and self.file_sources["file_path"]["path"] == [[]]
            and self.file_sources["file_list"] == [[]]
        ):
            raise ResultsProcessingError(
                "No file sources given. File sources must be given for writing results to database."
            )
        # start MP process
        logging.debug(self.file_sources)

        # NOTE: if implementing a new parser manager (i.e. serial) must add it to this dict
        implemented_parser_managers = {
            "multiprocessing": MPManager,
        }
        parser_opts = {}
        for k, v in self.__dict__.items():
            if k == "parser_manager":
                continue
            parser_opts[k] = v
        self.parser = implemented_parser_managers[self.parser_manager](**parser_opts)
        self.parser.process_files()
