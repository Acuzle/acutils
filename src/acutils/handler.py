import numpy as np
import os

from . import file
from . import multiprocess
from . import sheet



class DataHandler:

    def __init__(self, datapath, file_extensions=None, allowed_cpus=1, seed=871):
        '''
        Initiate DataHandler instance to handle data on disk.
        \nPARAMETERS
          datapath (str): absolute path to the directory that contain source files
          file_extensions=None (array/list like of str): source file allowed extensions
          allowed_cpus=1 (int): maximum amount of cpus used to compute
          seed=871 (int): seed used to initialize numpy randomizer
        \nRAISES
          NotADirectoryError: if the absolute path doesn't lead to an existing directory
        '''
        if not os.path.isdir(datapath):
            raise NotADirectoryError("datapath must be an absolute path to an existing directory")
        
        self.datapath = datapath
        self.file_extensions = file_extensions
        self.allowed_cpus = allowed_cpus
        self.seed = seed
        self.files = None
        self.labels = None
        self.unique_labels = None


    def _format_sheet(self, df, filecol=None, labelcol=None, othercols=None, clueless_words=None):
        '''
        Format a dataframe by deleting rows with empty cell, also add extension to filenames
        if filename doesn't contain it already, and if there is only one extension.
        \nPARAMETERS
          df (pandas.DataFrame): dataframe to format
          filecol=None (str): name of the column that contains filenames, not used there
          labelcol=None (str): name of the column that contains labels, not used there
          othercols=None (list<str>): name of the other columns, not used there
          clueless_words=None (array/list like of str): strings considered as None
        \nRETURNS
          df (pandas.DataFrame): formated dataframe
        '''
        return sheet.delete_clueless_rows(df, clueless_words)


    def _load_sheet(self, sheetpath, filecol, labelcol, othercols=None):
        '''
        Load a sheet file and keep indicated columns.
        \nPARAMETERS
          sheetpath (str): absolute path to the sheet which contain information about data
          filecol=None (str): name of the column that contains filenames
          labelcol=None (str): name of the column that contains labels, not used here
          othercols=None (iterable of str): name of the other columns to keep
        \nRETURNS
          df: (pandas.DataFrame) loaded dataframe
        \nRAISES
          ValueError: If the file extension is not supported.
        '''
        if othercols is None:
            othercols = []
        cols = [col for col in othercols]
        cols.append(filecol) ; cols.append(labelcol)
        return sheet.read_df_from_any_avalaible_extensions(sheetpath)[cols]


    # def load_labeled_data_fromsheet(self, sheetpath, filecol, labelcol, othercols=None, 
    #         clueless_words=None):
    #     '''
    #     Load data files and labels from a sheet file.
    #     \nPARAMETERS
    #       sheetpath (str): absolute path to the sheet which contain information about data
    #       filecol=None (str): name of the column that contains filenames
    #       labelcol=None (str): name of the column that contains labels, not used here
    #       othercols=None (array/list like of str): name of the other columns to keep
    #       clueless_words=None (array/list like of str): strings considered as None
    #     '''
    #     # Load and format sheet
    #     df = self._load_sheet(sheetpath, filecol, labelcol, othercols)
    #     df[filecol] = df[filecol].astype(str)
    #     df[labelcol] = df[labelcol].astype(str)
    #     df = self._format_sheet(df, filecol, labelcol, othercols, clueless_words)

    #     # Update files and labels
    #     if df.size == 0:
    #         print('|WRN| no file or label keeped, nothing changed. Leaving.')
    #     else:
    #         self.files = df[filecol].values
    #         self.labels = df[labelcol].values
    #         self.unique_labels = np.unique(self.labels)


    def load_data_fromdatapath(self):
        '''
        Load data files from data directory.
        Assuming that those files are directly inside the data directory.
        '''
        anyfile = (self.file_extensions is None 
                   or len(self.file_extensions) == 0) # if no extension, keep any extensions
        self.files = np.array([filename for filename in os.listdir(self.datapath) 
                              if anyfile or filename.endswith(tuple(self.file_extensions))])


    def load_labels_fromsheet(self, sheetpath, idcol, labelcol, 
        othercols=None, clueless_words=None, delete_unlabeled_files=True):
        '''
        Load data labels from a sheet file. 
        You must load files before calling this, you might call "load_data_fromdatapath".
        \nPARAMETERS
          sheetpath (str): absolute path to the sheet which contain information about data
          idcol=None (str): name of the column that contains at least a part of the filename
          labelcol=None (str): name of the column that contains labels, not used here
          othercols=None (array/list like of str): name of the other columns to keep
          clueless_words=None (array/list like of str): strings considered as None
          delete_unlabeled_files=True (bool): if True, delete each file without label
        '''
        # Load and format sheet
        df = self._load_sheet(sheetpath, idcol, labelcol, othercols)
        df[idcol] = df[idcol].astype(str)
        df[labelcol] = df[labelcol].astype(str)
        df = self._format_sheet(df, idcol, labelcol, othercols, clueless_words)

        # Browse files through the size of those names (descending order)
        # So if a smaller is included inside a bigger, its exit before disturbing
        indices = np.argsort(np.array([len(idstr) for idstr in df[idcol].values]))
        df = df.reindex(index=indices[::-1])

        # Get the label of each corresponding file
        labels = np.empty(self.files.shape, dtype=f'U128')
        for i, filename in enumerate(self.files):
            for filepart, label in zip(df[idcol].values, df[labelcol].values):
                if filepart in filename:
                    labels[i] = label
                    break
        
        # Update labels
        if np.all(labels == ''):
            print('|WRN| no label keeped, nothing changed. Leaving.')
        else:
            if delete_unlabeled_files:
                ids = np.where(labels != '')[0]
                self.files = self.files[ids]
                self.labels = labels[ids]
            else:
                self.labels = labels
            self.unique_labels = np.unique(self.labels)


    def load_labeled_data_fromdatapath(self):
        '''
        Load data files and labels from data directory.
        Assuming that those files are inside subdirectories (named with unique labels).
        '''
        # Init arrays
        unique_labels = np.array([label for label in os.listdir(self.datapath) 
                                  if os.path.isdir(os.path.join(self.datapath, label))])
        labels = np.array([], dtype='U')
        files = np.array([], dtype='U')

        # Fill them label per label with founded files (if the extension is allowed)
        anyfile = (self.file_extensions is None 
                   or len(self.file_extensions) == 0) # if no extension, keep any extensions
        for i, label in enumerate(unique_labels):
            incoming_files = np.array([os.path.join(label, filename) for filename in os.listdir(
                    os.path.join(self.datapath, label)) if anyfile or filename.endswith(
                                                            tuple(self.file_extensions))])
            if incoming_files.size == 0:
                del unique_labels[i] # a label without data is useless
                continue
            files = np.concatenate([files, incoming_files])
            labels = np.concatenate([labels, 
                                np.repeat(np.array([label]), incoming_files.size)])
        
        # Update attributes only if not empty
        if files.size == 0 or labels.size == 0 or unique_labels.size == 0:
            print('|WRN| no file or label keeped, nothing changed. Leaving.')
        else:
            self.unique_labels = unique_labels
            self.labels = labels
            self.files = files
    

    def load_groups_fromsheet(self, sheetpath, idcol, groupcol, clueless_words=None):
        '''
        Load data groups from a sheet file. 
        You must load files before calling this, you might call "load_data_fromdatapath".
        \nPARAMETERS
          sheetpath (str): absolute path to the sheet which contain information about data
          idcol=None (str): name of the column that contains at least a part of the filename
          groupcol=None (str): name of the column that contains groups, not used here
          clueless_words=None (array/list like of str): strings considered as None
        '''
        # Load and format sheet
        df = sheet.read_df_from_any_avalaible_extensions(sheetpath)
        df[idcol] = df[idcol].astype(str)
        df[groupcol] = df[groupcol].astype(str)

        # Be sure that '' is considered as empty
        if clueless_words is None:
            clueless_words = ['']
        else:
            clueless_words = [word for word in clueless_words]

        # Browse files through the size of those names (descending order)
        # So if a smaller is included inside a bigger, its exit before disturbing
        indices = np.argsort(np.array([len(idstr) for idstr in df[idcol].values]))
        df = df.reindex(index=indices[::-1])

        # Get the group of each corresponding file (if avalaible)
        groups = np.empty(self.files.shape, dtype=f'U128')
        for i, filename in enumerate(self.files):
            groups[i] = filename # in case no group found, filename becomes the group
            for filepart, group in zip(df[idcol].values, df[groupcol].values):
                if filepart in filename:
                    groups[i] = group if group not in clueless_words else filename
                    break
        self.groups = groups


    def _balance_dataset(self, data):
        '''
        Balance dataset so the amount of data is equal for each label.
        \nPARAMETERS
          data (dict<str,str>): dictionary with filename as key and label as value
        \nRETURNS
          balanced_data (dict<str,str>): data without superfluous files to balance it
        '''
        balanced_data = data.copy()

        # Check how much data should be keeped (amout of the label with the less data)
        files = np.array(list(balanced_data.keys()))
        labels = np.array(list(balanced_data.values()))
        lengths = np.array([np.where(labels == label)[0].size for label in self.unique_labels])
        keeped_data = np.min(lengths[np.nonzero(lengths)]) # if no data, must be an error
        
        # Balance data for each label
        for length, label in zip(lengths, self.unique_labels):
            diff = length - keeped_data # find how much data should be deleted
            if diff > 0:
                ids = np.where(labels == label)[0]
                np.random.seed(self.seed) # so the balance is repeatable
                np.random.shuffle(ids) # but still random
                for filename in files[ids][:diff]: # delete "diff" files from this label
                    del balanced_data[filename]

        return balanced_data


    def balance_datasets(self, tdata, vdata):
        '''
        Balance datasets so the amount of data is equal for each label.
        This is basically calling "_balance_dataset" method with tdata then vdata.
        \nPARAMETERS
          tdata (dict<str,str>): train dictionary with filename as key and label as value
          vdata (dict<str,str>): val dictionary with filename as key and label as value
        \nRETURNS
          balanced_tdata (dict<str,str>): train data without superfluous files to balance it
          balanced_vdata (dict<str,str>): val data without superfluous files to balance it
        '''
        return self._balance_dataset(tdata), self._balance_dataset(vdata)


    def split(self, train_percentage=0.7, balance=False):
        '''
        Split labeled data into train and test datasets.
        \nPARAMETERS
          train_percentage=0.7 (float): percentage of data expected in train dataset
          balance=False (bool): do call "balance_datasets" method before returning dictionaries
        \nRETURNS
          tdata (dict<str,str>): train dictionary with filename as key and label as value
          vdata (dict<str,str>): val dictionary with filename as key and label as value
        '''
        if self.files is None or self.labels is None or self.unique_labels is None:
            print('|WRN| Load labeled data before calling "split". '
                  '"files", "labels" and "unique_labels" attributes shouldn\'t be None. '
                  'Leaving.')
            return None
        
        if train_percentage < 0 or train_percentage > 1:
            print('|WRN| should be: 0.00 <= "train_percentage" <= 1.00. Leaving.')
            return None

        # Init arrays to store train/val files and labels
        train_files, train_labels = np.array([], dtype='U'), np.array([], dtype='U')
        val_files, val_labels = np.array([], dtype='U'), np.array([], dtype='U')
        val_percentage = 1 - train_percentage

        # Fill train/val files and labels label per label referring to train_percentage
        for label in self.unique_labels:
            ids = np.where(self.labels == label)[0]
            np.random.seed(self.seed) # so the split is repeatable
            np.random.shuffle(ids) # but still random
            startsat = int(np.ceil(ids.size*val_percentage))
            train_files = np.concatenate([train_files, self.files[ids[startsat:]]])
            train_labels = np.concatenate([train_labels, self.labels[ids[startsat:]]])
            val_files = np.concatenate([val_files, self.files[ids[:startsat]]])
            val_labels = np.concatenate([val_labels, self.labels[ids[:startsat]]])
        
        # Store files and labels inside dictionaries (tdata for train, vdata for val)
        tdata = {filename: label for filename, label in zip(train_files, train_labels)}
        vdata = {filename: label for filename, label in zip(val_files, val_labels)}

        # Balance datasets (if required)
        if balance:
            tdata, vdata = self.balance_datasets(tdata, vdata)

        return tdata, vdata


    def split_using_groups(self, train_percentage=0.7, balance=False):
        '''
        Split labeled data into train and test datasets considering data groups.
        \nPARAMETERS
          train_percentage=0.7 (float): percentage of data expected in train dataset
          balance=False (bool): do call "balance_datasets" method before returning dictionaries
        \nRETURNS
          tdata (dict<str,str>): train dictionary with filename as key and label as value
          vdata (dict<str,str>): val dictionary with filename as key and label as value
        '''
        if self.files is None or self.labels is None or self.unique_labels is None:
            print('|WRN| Load labeled data before calling "split". '
                  '"files", "labels" and "unique_labels" attributes shouldn\'t be None. '
                  'Leaving.')
            return None
        
        if self.groups is None:
            print('|WRN| Load groups before calling "split".')
            return None
        
        if train_percentage < 0 or train_percentage > 1:
            print('|WRN| should be: 0.00 <= "train_percentage" <= 1.00. Leaving.')
            return None

        # Init lists to store train/val files and labels
        train_files, train_labels = [], []
        val_files, val_labels = [], []

        # Fill train/val files and labels label per label referring to train_percentage
        for label in self.unique_labels:
            # Get groups for data with this label
            iftl = np.where(self.labels == label)[0] # indices for this label
            unique_groups, _, counts = np.unique(self.groups[iftl], return_index=True, 
                                           return_counts=True)

            # Shuffle to split it randomly
            np.random.seed(self.seed) # so the split is repeatable
            browsing_order = np.random.choice(unique_groups.shape[0], 
                                              size=unique_groups.shape[0], 
                                              replace = False).astype(np.uint64)

            # Split data using file amounts (but still considering groups)
            quantity = 0
            train_cap = train_percentage * iftl.shape[0]
            for i in browsing_order:
                positions = np.where(self.groups[iftl] == unique_groups[i])[0]
                for pos in positions: # contains each file index of the same group
                    if quantity <= train_cap:
                        train_files.append(self.files[iftl][pos])
                        train_labels.append(self.labels[iftl][pos])
                    else: # fill val only if train is full
                        val_files.append(self.files[iftl][pos])
                        val_labels.append(self.labels[iftl][pos])
                quantity += counts[i]
        
        # Store files and labels inside dictionaries (tdata for train, vdata for val)
        tdata = {filename: label for filename, label in zip(train_files, train_labels)}
        vdata = {filename: label for filename, label in zip(val_files, val_labels)}

        # Balance datasets (if required)
        if balance:
            tdata, vdata = self.balance_datasets(tdata, vdata)

        return tdata, vdata


    def _distribute_data(self, dirpath):
        '''
        Distribute files to process and split them between allowed cpus.
        The distribution is returned as 2 lists of lists of src or dstdir.
        \nPARAMETERS
          dirpath (str): absolute path to the directory for treated files
        \nRETURNS
          packed_srcs (list<list<str>>): source files absolute paths per process
          packed_dstdirs (list<list<str>>): destination directories absolute paths per process
        '''
        # Update destination directory with labels (if defined)
        if self.labels is not None:
            dstdirs = np.array([os.path.join(dirpath, label) for label in self.labels])
        else:
            dstdirs = np.array([dirpath for _ in range(self.files.size)])
          
        # Take file absolute paths
        srcs = np.array([os.path.join(self.datapath, filename) for filename in self.files])
        
        # Pack src files and directories for multiprocessing
        packed_srcs, packed_dstdirs = multiprocess.distribute(srcs,
                               dstdirs, self.allowed_cpus, self.seed)
        return packed_srcs, packed_dstdirs


    def _distribute_datasets(self, tdstdir, vdstdir, tdata, vdata):
        '''
        Distribute files to process and split them between allowed cpus.
        The distribution is returned into collections.
        \nPARAMETERS
          tdstdir (str): absolute path to the destination files directory for train dataset
          vdstdir (str): absolute path to the destination files directory for val dataset
          tdata (dict<str,str>): train dictionary with filename as key and label as value
          vdata (dict<str,str>): val dictionary with filename as key and label as value
        \nRETURNS
          packed_srcs (list<list<str>>): src files absolute paths per process
          packed_dstdirs (list<list<str>>): destination directories absolute paths per process
        '''
        # Define srcs and dstdirs
        srcs, dstdirs = [], []
        for data, dirpath in zip([tdata, vdata], [tdstdir, vdstdir]):
            for filename, label in data.items():
                srcs.append(os.path.join(self.datapath, filename))
                dstdirs.append(os.path.join(dirpath, label))
        srcs = np.array(srcs)
        dstdirs = np.array(dstdirs)

        # Pack src files and directories for multiprocessing
        packed_srcs, packed_dstdirs = multiprocess.distribute(srcs, 
                              dstdirs, self.allowed_cpus, self.seed)
        return packed_srcs, packed_dstdirs


    def _run_processes(self, packed_srcs, packed_dstdirs, func, **kwargs):
        '''
        Run processes on the maximum amount of allowed cpus to apply "func" function to each
        source file.
        "func" needs "src" and "dstdir" params (in acutils, those are prefixed with "tmnt").
        **kwargs should be addionnal arguments to pass to the "func" function.
        \nPARAMETERS
          packed_srcs (array/list like of iterables of str): src files absolute paths per process
          packed_dstdirs (array/list like of iterables of str): dst dirs absolute paths per process
          func (function): treatment that will be applied on each source file
                           it needs an absolute path to the source file "src" 
                           and absolute absolute path to destination files directory "dstdir"
                           in acutils, any function prefixed with "tmnt" is usable
                           **kwargs: arguments to pass to the "func" function
        '''
        multiprocess.run_processes_on_multiple_files(packed_srcs, 
                  packed_dstdirs, func, self.allowed_cpus, **kwargs)


    def _reset_directory(self, dirpath):
        '''
        Delete directory if it exists, then create it again and fill it with
        empty subdirecories, named from unique labels (if defined and not empty).
        \nPARAMETERS
          dirpath (str): absolute path to the directory to reset
        '''
        file.reset_directory(dirpath, subs=self.unique_labels)


    def process(self, dirpath, func=None, empty_dir=True, **kwargs):
        '''
        Run processes on the maximum amount of allowed cpus to apply "func" function to each
        source file.
        "func" needs "src" and "dstdir" params (in acutils, those are prefixed with "tmnt").
        **kwargs should be addionnal arguments to pass to the "func" function.
        \nPARAMETERS
          dirpath (str): absolute path to treated files directory
          func=None (function): treatment that will be applied on each source file
                                it needs an absolute path to the source file "src" 
                                and absolute absolute path to destination files directory "dstdir"
                                if None, source files will be copied to the destination directory
                                in acutils, any function prefixed with "tmnt" is usable
          empty_dir=True (bool): if True, reset destination directory and fill it with unique labels
                          as subdirectories if defined
          **kwargs: arguments to pass to the "func" function
        '''
        # Without treatment to apply, copy source files
        if func is None:
            func = file.tmnt_copyfile_to_dir
        
        # Reset treated files directory 
        if empty_dir:
            self._reset_directory(dirpath)

        # Distribute files between cpus and run processes
        packed_srcs, packed_dstdirs = self._distribute_data(dirpath)
        self._run_processes(packed_srcs, packed_dstdirs, func, **kwargs)


    def make_datasets(self, trainpath, valpath, tdata, vdata, func=None, empty_dir=True, **kwargs):
        '''
        Run processes on the maximum amount of allowed cpus to apply "func" function to each
        source file.
        "func" needs "src" and "dstdir" params (in acutils, those are prefixed with "tmnt").
        **kwargs should be addionnal arguments to pass to the "func" function.
        \nPARAMETERS
          trainpath (str): absolute path to the destination files train directory
          valpath (str): absolute path to the destination files val directory
          tdata (dict<str,str>): train dictionary with filename as key and label as value
          vdata (dict<str,str>): val dictionary with filename as key and label as value
          func=None (function): treatment that will be applied on each source file
                                it needs an absolute path to the source file "src" 
                                and absolute absolute path to destination files directory "dstdir"
                                if None, source files will be copied to the destination directory
                                in acutils, any function prefixed with "tmnt" is usable
          empty_dir=True (bool): if True, reset destination directories and fill it with unique labels
                                 as subdirectories if defined
          **kwargs: arguments to pass to the "func" function
        '''
        # Without treatment to apply, copy source files
        if func is None:
            func = file.tmnt_copyfile_to_dir
        
        # Reset train and val directories
        if empty_dir:
            self._reset_directory(trainpath)
            self._reset_directory(valpath)

        # Distribute files between cpus and run processes
        packed_srcs, packed_dstdirs = self._distribute_datasets(trainpath, valpath, tdata, vdata)
        self._run_processes(packed_srcs, packed_dstdirs, func, **kwargs)