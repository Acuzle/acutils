import numpy as np
import os

from . import file
from . import multiprocess
from . import sheet



class DataHandler:
    '''
    Main class to handle data on disk.

    ATTRIBUTES
    ----------
    (str) datapath:
        Absolute path to the directory that contain source files.
    
    (array/list like of str) file_extensions=None:
        Source file allowed extensions.
    
    (int) allowed_cpus=1:
        Maximum amount of CPUs used to compute.
    
    (int) seed=871:
        Seed used to initialize numpy randomizer.
    
    (str) str_ndarray_dtype="U256":
        Data type used for any string numpy arrays. It defines the maximum 
            length of strings, especially those in sheet files, for loading 
            labels and groups.
    
    (numpy.array<str_ndarray_dtype>) files=None:
        The filenames (with extension) of the files to load.
    
    (numpy.array<str_ndarray_dtype>) labels=None:
        The labels of the files.
    
    (numpy.array<str_ndarray_dtype>) unique_labels=None:
        The unique labels among the labels.
    
    (numpy.array<str_ndarray_dtype>) groups=None:
        The groups of the files, all with the same will be in the same dataset split.
    '''

    def __init__(self, datapath, file_extensions=None, allowed_cpus=1, seed=871,
                 str_ndarray_dtype="U256"):
        '''
        Initiate DataHandler instance to handle data on disk.

        PARAMETERS
        ----------        
		(str) datapath:
		    Absolute path to the directory that contain source files.
        
		(array/list like of str) file_extensions=None:
		    Source file allowed extensions.
        
		(int) allowed_cpus=1:
		    Maximum amount of CPUs used to compute.
        
		(int) seed=871:
		    Seed used to initialize numpy randomizer.
        
		(str) str_ndarray_dtype="U256":
		    Data type used for any string numpy arrays. It defines the maximum 
                length of strings, especially those in sheet files, for loading 
                labels and groups.
    
        RETURNS
        -------
		None
        
        RAISES
        ------
        (NotADirectoryError) err: 
            if the absolute path doesn't lead to an existing directory.
        '''
        if not os.path.isdir(datapath):
            raise NotADirectoryError("datapath must be an absolute path to an "
                                     "existing directory")
        
        self.datapath = datapath
        self.file_extensions = file_extensions
        self.allowed_cpus = allowed_cpus
        self.seed = seed
        self.str_ndarray_dtype = str_ndarray_dtype
        self.files = None
        self.labels = None
        self.unique_labels = None
        self.groups = None


    def _format_sheet(self, df, filecol=None, labelcol=None, othercols=None, 
                      clueless_words=None):
        '''
        Format a dataframe by deleting rows with empty cell, also add extension 
        to filenames if filename doesn't contain it already, and if there is 
        only one extension.

        PARAMETERS
        ----------        
		(pandas.DataFrame) df:
		    dataframe to format
        
		(str) filecol=None:
		    Name of the column that contains filenames, not used there.
        
		(str) labelcol=None:
		    Name of the column that contains labels, not used there.
        
		(list<str>) othercols=None:
		    Name of the other columns, not used there.
        
		(array/list like of str) clueless_words=None:
		    Strings considered as None.

        RETURNS
        -------        
		(pandas.DataFrame) df:
		    formated dataframe.
    
        RAISES
        ------
        None
        '''
        return sheet.delete_clueless_rows(df, clueless_words)


    def _load_sheet(self, sheetpath, filecol, labelcol, othercols=None):
        '''
        Load a sheet file and keep indicated columns.

        PARAMETERS
        ----------        
		(str) sheetpath:
		    Absolute path to the sheet which contain information about data.
        
		(str) filecol=None:
		    Name of the column that contains filenames.
        
		(str) labelcol=None:
		    Name of the column that contains labels, not used here.
        
		(iterable of str) othercols=None:
		    Name of the other columns to keep.

        RETURNS
        -------        
		(pandas.DataFrame) df:
		    Loaded dataframe.

        RAISES
        ------
        (ValueError) err:
            If the file extension is not supported.
        '''
        if othercols is None:
            othercols = []
        cols = [col for col in othercols]
        cols.append(filecol) ; cols.append(labelcol)
        return sheet.read_df_from_any_avalaible_extensions(sheetpath)[cols]


    def load_data_fromdatapath(self):
        '''
        Load data files from data directory.
        Assuming that those files are directly inside the data directory.
        The filenames are stored as "files" attribute.

        PARAMETERS
        ----------
		None
    
        RETURNS
        -------
		None
        '''
        anyfile = (self.file_extensions is None # if no extension, keep any
                   or len(self.file_extensions) == 0) 
        self.files = np.array([filename for filename in os.listdir(self.datapath) 
                              if anyfile 
                              or filename.endswith(tuple(self.file_extensions))],
                              dtype=self.str_ndarray_dtype)


    def load_labels_fromsheet(self, sheetpath, idcol, labelcol, 
            othercols=None, clueless_words=None, delete_unlabeled_files=True,
            require_full_filename_match=False):
        '''
        Load data labels from a sheet file. 
        You must load files before calling this, you might call 
        "load_data_fromdatapath". The labels are stored as "labels" attribute 
        and their unique values are stored as "unique_labels" attribute.

        PARAMETERS
        ----------        
		(str) sheetpath:
		    Absolute path to the sheet which contain information about data.
        
		(str) idcol=None:
		    Name of the column that contains at least a part of the filename.
        
		(str) labelcol=None:
		    Name of the column that contains labels, not used here.
        
		(array/list like of str) othercols=None:
		    Name of the other columns to keep.
        
		(array/list like of str) clueless_words=None:
		    Strings considered as None.
        
		(bool) delete_unlabeled_files=True:
		    If True, delete each file without label.
        
		(bool) require_full_filename_match=False:
		    If True, requires the value in the idcol to be exactly the filename,
            otherwise, if the value in the idcol is included in the filename, 
            it is considered as a match. Note that if the idcol value is 
            included in multiple filenames, it will be associated with the 
            first one found, in descending length order.
    
        RETURNS
        -------
		None
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
        labels = np.empty(self.files.shape, dtype=self.str_ndarray_dtype)
        for i, filename in enumerate(self.files):
            for filepart, label in zip(df[idcol].values, df[labelcol].values):
                if filepart in filename:
                    if require_full_filename_match and filepart != filename:
                        continue
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
            self.unique_labels = np.unique(self.labels
                                           ).astype(self.str_ndarray_dtype)


    def load_labeled_data_fromdatapath(self):
        '''
        Load data files and labels from data directory.
        Assuming that those files are inside subdirectories (named with unique 
        labels). The filenames are stored as "files" attribute. The labels are 
        stored as "labels" attribute and their unique values are stored as 
        "unique_labels" attribute.

        PARAMETERS
        ----------
		None
    
        RETURNS
        -------
		None
        '''
        # Init arrays
        unique_labels = np.array([label for label in os.listdir(self.datapath) 
                            if os.path.isdir(os.path.join(self.datapath, label))],
                            dtype=self.str_ndarray_dtype)
        labels = np.array([], dtype=self.str_ndarray_dtype)
        files = np.array([], dtype=self.str_ndarray_dtype)

        # Fill them label per label with founded files (if the ext is allowed)
        anyfile = (self.file_extensions is None # if no extension, keep any
                   or len(self.file_extensions) == 0) 
        for i, label in enumerate(unique_labels):
            incoming_files = np.array(
                [os.path.join(label, filename) for filename in os.listdir(
                    os.path.join(self.datapath, label)) 
                    if anyfile or filename.endswith(tuple(self.file_extensions)
                )]
            )
            if incoming_files.size == 0:
                del unique_labels[i] # a label without data is useless
                continue
            files = np.concatenate([files, incoming_files])
            labels = np.concatenate([labels, 
                            np.repeat(np.array([label]), incoming_files.size)]
            ).astype(self.str_ndarray_dtype)
        
        # Update attributes only if not empty
        if files.size == 0 or labels.size == 0 or unique_labels.size == 0:
            print('|WRN| no file or label keeped, nothing changed. Leaving.')
        else:
            self.unique_labels = unique_labels
            self.labels = labels
            self.files = files
    

    def load_groups_fromsheet(self, sheetpath, idcol, groupcol, 
            clueless_words=None, require_full_filename_match=False):
        '''
        Load data groups from a sheet file. 
        You must load files before calling this, you might call 
        "load_data_fromdatapath". The groups are stored as "groups" attribute.

        PARAMETERS
        ----------        
		(str) sheetpath:
		    Absolute path to the sheet which contain information about data.
        
		(str) idcol=None:
		    Name of the column that contains at least a part of the filename.
        
		(str) groupcol=None:
		    Name of the column that contains groups, not used here.
        
		(array/list like of str) clueless_words=None:
		    Strings considered as None.
        
		(bool) require_full_filename_match=False:
		    If True, requires the value in the idcol to be exactly the filename,
            otherwise, if the value in the idcol is included in the filename, 
            it is considered as a match. Note that if the idcol value is 
            included in multiple filenames, it will be associated with the 
            first one found, in descending length order.
    
        RETURNS
        -------
		None
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
        groups = np.empty(self.files.shape, dtype=self.str_ndarray_dtype)
        for i, filename in enumerate(self.files):
            groups[i] = filename # in case no group, filename becomes the group
            for filepart, group in zip(df[idcol].values, df[groupcol].values):
                if filepart in filename:
                    if require_full_filename_match and filepart != filename:
                        continue
                    groups[i] = (group 
                                 if group not in clueless_words 
                                 else filename)
                    break
        self.groups = groups


    def _balance_dataset(self, data):
        '''
        Balance dataset so the amount of data is equal for each label.

        PARAMETERS
        ----------        
		(dict<str;str>) data:
		    Dictionary with filename as key and label as value.

        RETURNS
        -------        
		(dict<str;str>) balanced_data:
		    Data without superfluous files to balance it.
        '''
        balanced_data = data.copy()

        # Check how much data should be keeped (amout of labels with less data)
        files = np.array(list(balanced_data.keys()))
        labels = np.array(list(balanced_data.values()))
        lengths = np.array(
             [np.where(labels == label)[0].size for label in self.unique_labels])
        keeped_data = np.min(lengths[np.nonzero(lengths)]) # if no data, error
        
        # Balance data for each label
        for length, label in zip(lengths, self.unique_labels):
            diff = length - keeped_data # find how much data should be deleted
            if diff > 0:
                ids = np.where(labels == label)[0]
                np.random.seed(self.seed) # so the balance is repeatable
                np.random.shuffle(ids) # but still random
                # delete "diff" files from this label
                for filename in files[ids][:diff]:
                    del balanced_data[filename]

        return balanced_data


    def balance_datasets(self, tdata, vdata):
        '''
        Balance datasets so the amount of data is equal for each label.
        This is basically calling "_balance_dataset" method with tdata then vdata.

        PARAMETERS
        ----------        
		(dict<str;str>) tdata:
		    Train dictionary with filename as key and label as value.
        
		(dict<str;str>) vdata:
		    Val dictionary with filename as key and label as value.

        RETURNS
        -------        
		(dict<str;str>) balanced_tdata:
		    Train data without superfluous files to balance it.
        
		(dict<str;str>) balanced_vdata:
		    Val data without superfluous files to balance it.
        '''
        return self._balance_dataset(tdata), self._balance_dataset(vdata)


    def _split_using_groups(self, train_percentage=0.7, balance=False):
        '''
        Split labeled data into train and test datasets considering data groups.

        PARAMETERS
        ----------        
		(float) train_percentage=0.7:
		    Percentage of data expected in train dataset.
        
		(bool) balance=False:
		    Do call "balance_datasets" method before returning dictionaries.

        RETURNS
        -------        
		(dict<str;str>) tdata:
		    Train dictionary with filename as key and label as value.
        
		(dict<str;str>) vdata:
		    Val dictionary with filename as key and label as value.
        '''
        if (self.files is None or self.labels is None 
            or self.unique_labels is None):
            print('|WRN| Load labeled data before calling "split". '
                  '"files", "labels" and "unique_labels" attributes should not '
                  'be None. Leaving.')
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

        # Fill train/val files/labels lab per lab referring to train_percentage
        for label in self.unique_labels:
            # Get groups for data with this label
            iftl = np.where(self.labels == label)[0] # indices for this label
            unique_groups, _, counts = np.unique(self.groups[iftl], 
                                                 return_index=True, 
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
                for pos in positions: # contains each file index of the same grp
                    if quantity <= train_cap:
                        train_files.append(self.files[iftl][pos])
                        train_labels.append(self.labels[iftl][pos])
                    else: # fill val only if train is full
                        val_files.append(self.files[iftl][pos])
                        val_labels.append(self.labels[iftl][pos])
                quantity += counts[i]
        
        # Store files and labels inside dictionaries (tdata for train, 
        # vdata for val)
        tdata = {filename: label for filename, label in 
                                        zip(train_files, train_labels)}
        vdata = {filename: label for filename, label in 
                                        zip(val_files, val_labels)}

        # Balance datasets (if required)
        if balance:
            tdata, vdata = self.balance_datasets(tdata, vdata)

        return tdata, vdata
    

    # @TODO maybe add an optional val_percentage and define a test set
    def split(self, train_percentage=0.7, balance=False, ignore_groups=False):
        '''
        Split labeled data into train and test datasets.

        PARAMETERS
        ----------        
		(float) train_percentage=0.7:
		    Percentage of data expected in train dataset.
        
		(bool) balance=False:
		    Do call "balance_datasets" method before returning dictionaries.
        
		(bool) ignore_groups=False:
            If True, ignore groups for the split, even though it is defined. 
            If the "groups" attribute is not define, then it is ignored anyway. 
            If it is defined and "ignore_groups" is False, then the split is done 
            calling "_split_using_groups" method.

        RETURNS
        -------        
		(dict<str;str>) tdata:
		    train dictionary with filename as key and label as value.
        
		(dict<str;str>) vdata:
		    val dictionary with filename as key and label as value.
        '''
        if (self.files is None or self.labels is None 
            or self.unique_labels is None):
            print('|WRN| Load labeled data before calling "split". '
                  '"files", "labels" and "unique_labels" attributes should '
                  'not be None. Leaving.')
            return None
        
        if train_percentage < 0 or train_percentage > 1:
            print('|WRN| Should be: 0.00 <= "train_percentage" <= 1.00. Leaving.')
            return None
        
        if not ignore_groups and self.groups is not None:
            return self._split_using_groups(train_percentage, balance)

        # Init arrays to store train/val files and labels
        train_files = np.array([], dtype=self.str_ndarray_dtype)
        train_labels = np.array([], dtype=self.str_ndarray_dtype)
        val_files = np.array([], dtype=self.str_ndarray_dtype)
        val_labels = np.array([], dtype=self.str_ndarray_dtype)
        val_percentage = 1 - train_percentage

        # Fill train/val files/labels lab per lab referring to train_percentage
        for label in self.unique_labels:
            ids = np.where(self.labels == label)[0]
            np.random.seed(self.seed) # so the split is repeatable
            np.random.shuffle(ids) # but still random
            startsat = int(np.ceil(ids.size*val_percentage))
            train_files = np.concatenate([train_files, 
                                          self.files[ids[startsat:]]])
            train_labels = np.concatenate([train_labels, 
                                           self.labels[ids[startsat:]]])
            val_files = np.concatenate([val_files, self.files[ids[:startsat]]])
            val_labels = np.concatenate([val_labels, self.labels[ids[:startsat]]])
        
        # Store files and labels inside dictionaries (tdata for train,
        # vdata for val)
        tdata = {filename: label for filename, label in 
                                        zip(train_files, train_labels)}
        vdata = {filename: label for filename, label in 
                                        zip(val_files, val_labels)}

        # Balance datasets (if required)
        if balance:
            tdata, vdata = self.balance_datasets(tdata, vdata)

        return tdata, vdata


    def _distribute_data(self, dirpath):
        '''
        Distribute files to process and split them between allowed cpus.
        The distribution is returned as 2 lists of lists of src or dstdir.

        PARAMETERS
        ----------        
		(str) dirpath:
		    Absolute path to the directory for treated files.

        RETURNS
        -------        
		(list<list<str>>) packed_srcs:
		    Source files absolute paths per process.
        
		(list<list<str>>) packed_dstdirs:
		    Destination directories absolute paths per process.
        '''
        # Update destination directory with labels (if defined)
        if self.labels is not None:
            dstdirs = np.array(
                [os.path.join(dirpath, label) for label in self.labels])
        else:
            dstdirs = np.array([dirpath for _ in range(self.files.size)])
          
        # Take file absolute paths
        srcs = np.array(
            [os.path.join(self.datapath, filename) for filename in self.files])
        
        # Pack src files and directories for multiprocessing
        packed_srcs, packed_dstdirs = multiprocess.distribute(srcs,
                               dstdirs, self.allowed_cpus, self.seed)
        return packed_srcs, packed_dstdirs


    def _distribute_datasets(self, tdstdir, vdstdir, tdata, vdata):
        '''
        Distribute files to process and split them between allowed cpus.
        The distribution is returned into collections.

        PARAMETERS
        ----------        
		(str) tdstdir:
		    Absolute path to the destination files directory for train dataset.
        
		(str) vdstdir:
		    Absolute path to the destination files directory for val dataset.
        
		(dict<str;str>) tdata:
		    Train dictionary with filename as key and label as value.
        
		(dict<str;str>) vdata:
		    Val dictionary with filename as key and label as value.

        RETURNS
        -------        
		(list<list<str>>) packed_srcs:
		    Src files absolute paths per process.
        
		(list<list<str>>) packed_dstdirs:
		    Destination directories absolute paths per process.
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
        Run processes on the maximum amount of allowed CPUs to apply "func" 
        function to each source file.
        "func" needs "src" and "dstdir" params (in acutils, those are 
        prefixed with "tmnt").
        **kwargs should be addionnal arguments to pass to the "func" function.

        PARAMETERS
        ----------        
		(array/list like of iterables of str) packed_srcs:
		    src files absolute paths per process.
        
		(array/list like of iterables of str) packed_dstdirs:
		    dst dirs absolute paths per process.
        
		(function) func:
            Treatment that will be applied on each source file
                it needs an absolute path to the source file "src" and absolute 
                path to destination files directory "dstdir". In acutils, 
                any function prefixed with "tmnt" is usable.

        **kwargs:
            Arguments to pass to the "func" function.
    
        RETURNS
        -------
		None
        '''
        multiprocess.run_processes_on_multiple_files(packed_srcs, 
                  packed_dstdirs, func, self.allowed_cpus, **kwargs)


    def _reset_directory(self, dirpath):
        '''
        Delete directory if it exists, then create it again and fill it with
        empty subdirecories, named from unique labels (if defined and not empty).

        PARAMETERS
        ----------        
		(str) dirpath:
		    Absolute path to the directory to reset.
    
        RETURNS
        -------
		None
        '''
        file.reset_directory(dirpath, subs=self.unique_labels)


    def process(self, dirpath, func=None, empty_dir=True, **kwargs):
        '''
        Run processes on the maximum amount of allowed CPUs to apply "func" 
        function to each source file. If "func" is None, just copy the file.
        "func" needs "src" and "dstdir" params (in acutils, those are 
        prefixed with "tmnt").
        **kwargs should be addionnal arguments to pass to the "func" function.

        PARAMETERS
        ----------        
		(str) dirpath:
		    Absolute path to treated files directory.
        
		(function) func=None:
            Treatment that will be applied on each source file it needs an 
            absolute path to the source file "src" and absolute path to 
            destination files directory "dstdir". In acutils, any 
            function prefixed with "tmnt" is usable.
                
		(bool) empty_dir=True:
		    If True, reset destination directory and fill it with unique labels
                as subdirectories if defined

        **kwargs:
            Arguments to pass to the "func" function.
    
        RETURNS
        -------
		None
        '''
        # Without treatment to apply, copy source files
        if func is None:
            func = file.tmnt_copyfile_to_dir
        
        # Reset treated files directory 
        if empty_dir:
            self._reset_directory(dirpath)

        # Distribute files between CPUs and run processes
        packed_srcs, packed_dstdirs = self._distribute_data(dirpath)
        self._run_processes(packed_srcs, packed_dstdirs, func, **kwargs)


    def make_datasets(self, trainpath, valpath, tdata, vdata, func=None, 
                      empty_dir=True, **kwargs):
        '''
        Run processes on the maximum amount of allowed CPUs to apply "func" 
        function to each source file.
        "func" needs "src" and "dstdir" params (in acutils, those are prefixed with "tmnt").
        **kwargs should be addionnal arguments to pass to the "func" function.

        PARAMETERS
        ----------        
		(str) trainpath:
		    Absolute path to the destination files train directory.
        
		(str) valpath:
		    Absolute path to the destination files val directory.
        
		(dict<str;str>) tdata:
		    Train dictionary with filename as key and label as value.
        
		(dict<str;str>) vdata:
		    Val dictionary with filename as key and label as value.
        
		(function) func=None:
            Treatment that will be applied on each source file it needs an 
            absolute path to the source file "src" and absolute path to 
            destination files directory "dstdir". In acutils, any 
            function prefixed with "tmnt" is usable.
        
		(bool) empty_dir=True:
		    If True, reset destination directories and fill it with unique labels 
            as subdirectories if defined.

        **kwargs: 
            Arguments to pass to the "func" function.
    
        RETURNS
        -------
		None
        '''
        # Without treatment to apply, copy source files
        if func is None:
            func = file.tmnt_copyfile_to_dir
        
        # Reset train and val directories
        if empty_dir:
            self._reset_directory(trainpath)
            self._reset_directory(valpath)

        # Distribute files between CPUs and run processes
        packed_srcs, packed_dstdirs = self._distribute_datasets(trainpath, 
                                                    valpath, tdata, vdata)
        self._run_processes(packed_srcs, packed_dstdirs, func, **kwargs)


    def save_split(self, dst, data):
        '''
        Save a split (from "split" method) as a json file.

        PARAMETERS
        ----------        
		(str) dst:
		    absolute path to the new json file.
        
		(dict<str;str>) data:
		    data dictionary to save.

        RETURNS
        -------
		None
        '''
        file.save_dict_as_json(dst, data)


    def load_split(src):
        '''
        Load a dictionary from a json file.

        PARAMETERS
        ----------        
		(str) src:
		    absolute path to the json file.

        RETURNS
        -------        
		(dict<str;str>) data:
		    loaded data dictionary.
        '''
        return file.load_dict_from_json(src)