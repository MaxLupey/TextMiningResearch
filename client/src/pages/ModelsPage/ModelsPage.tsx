import React, { FC, useContext, useEffect, useState } from "react"
import { AuthContext } from "../../api/contexts/AuthContext";
import ActionPanel from "../../elements/ActionPanel/ActionPanel";
import {
    Button,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableRow,
    Paper,
    IconButton,
    Checkbox,
    TablePagination,
    TableFooter,
    TableHead,
    TableSortLabel,
    FormControlLabel,
    Switch,
    Box,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogContentText,
    TextField,
    DialogActions,
    Alert,
    Backdrop,
    CircularProgress
} from "@mui/material";
import { visuallyHidden } from '@mui/utils';
import {
    GetApp as GetAppIcon,
    FileCopyOutlined as FileCopyOutlinedIcon,
    LockOpen as LockOpenIcon,
    Lock as LockIcon,
    Edit as EditIcon,
    Delete as DeleteIcon
} from '@mui/icons-material';
import {useNavigate} from "react-router-dom";
import {UploadFileInput} from "../../elements/UplodaFileInput/UploadFileInput";
import {useForm} from "react-hook-form";
import { tminginRequest } from "../../api/requests/tminingRequests";
import { urls, tminingUrl } from "../../api/routers/tminingRouters";

const ModelsPage: FC = () => {
    const { userData } = useContext(AuthContext);
    const [models, setModels] = useState<Array<any>>([]);
    const [selected, setSelected] = useState<Array<any>>([]);
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(10);
    const [order, setOrder] = useState<'asc' | 'desc'>('asc');
    const [orderBy, setOrderBy] = useState<keyof typeof models[0]>('name');
    const [alertText, setAlertText] = useState("");
    const [severity, setSeverity] = useState<"success" | "error" | "warning" | "info">("success");
    const [alertOpen, setAlertOpen] = useState(false);
    const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [uploadDialogOpen, setUploadDialogOpen] = useState(false);
    const [shared, setShared] = useState(false);
    const [currentModelName, setCurrentModelName] = useState("");
    const [currentShared, setCurrentShared] = useState(false);
    const { register, handleSubmit, formState: { errors } } = useForm();
    const [currentUUID, setCurrentUUID] = useState("");

    const onSubmit = (data: any) => {
        const formData = new FormData();
        let fileNameWithoutExtension = '';
        if (data.model) {
            fileNameWithoutExtension = data.model[0].name.split('.').slice(0, -1).join('.');
            formData.append('file', data?.model[0]);
        }

        let queries = {
            model_name: fileNameWithoutExtension,
            shared: shared
        }
        setUploadDialogOpen(false);
        tminginRequest.uploadModel(queries, formData)
            .then(response => {
                if (response.status === 200) {
                    alertTextMethod("Model uploaded successfully", "success");
                    fetchModels();
                }
                else {
                    throw new Error(response.data.message);
                }
            })
            .catch(error => {
                alertTextMethod("Failed to upload model: " + error, "error")
            });
    };

  const handleUploadClick = () => {
    setUploadDialogOpen(true);
  };

  const handleUploadDialogClose = () => {
    setUploadDialogOpen(false);
  };

  const handleSharedChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setShared(event.target.checked);
  };

    const handleDeleteConfirm = () => {
        setDeleteDialogOpen(false);
        deleteSelectedModels();
    };

    const handleDeleteDialogClose = () => {
        setDeleteDialogOpen(false);
    };

    const alertTextMethod = (text: string, severity: string) => {
        setAlertText(text);
        switch (severity) {
            case "error":
                setSeverity("error");
                break;
            case "success":
                setSeverity("success");
                break;
            case "warning":
                setSeverity("warning");
                break;
            case "info":
                setSeverity("info");
                break;
            default:
                throw new Error("Unknown severity: " + severity);
        }
        setAlertOpen(true);
    }

    const fetchModels = () => {
        if (userData) {
            setLoading(true);
            tminginRequest.getUserModels()
            .then(response => {
                setModels(response.data.models);
            })
            .catch(error => {
                console.error('Error fetching data: ', error);
            });
            setLoading(false);
        }
        setSelected([]);
    };

    useEffect(() => {
        if (!userData) {
            navigate('/');
        }
        fetchModels();
    }, [userData]);

    const [renameDialogOpen, setRenameDialogOpen] = useState(false);
    const [newModelName, setNewModelName] = useState("");

    const handleRenameClick = (uuid: string, name: string, shared: boolean) => {
        setCurrentUUID(uuid)
        setCurrentModelName(name);
        setCurrentShared(shared);
        setRenameDialogOpen(true);
    };

    const deleteModel = (modelUUID: string) => {
        tminginRequest.deleteModel(modelUUID)
            .then(response => {
                if (response.status === 200) {
                    alertTextMethod("Model deleted successfully", "success");
                    fetchModels();
                } else {
                    throw new Error(response.data.message);
                }
            })
            .catch(error => {
                throw new Error('Failed to delete model: ' + error);
            });
    };

    const deleteSelectedModels = () => {
        try {
            selected.forEach(modelUUID => {
                deleteModel(modelUUID);
            });
            alertTextMethod("Deleting selected models is finished", "success");
        } catch (error) {
            alertTextMethod("Failed to delete selected models: " + error, "error");
        }
    }

    const handleRenameConfirm = () => {
        let queries = {
            model_uuid: currentUUID,
            new_model_name: newModelName,
            shared: currentShared
        }

        const formData = new FormData();

        tminginRequest.editModel(queries, formData)
            .then(response => {
                if (response.status === 200) {
                    alertTextMethod("Model renamed successfully", "success");
                    fetchModels();
                } else {
                    throw new Error(response.data.message);
                }
            })
            .catch(error => {
                alertTextMethod("Failed to rename model: " + error, "error")
            });
        setRenameDialogOpen(false);
    };

    const handleRenameDialogClose = () => {
        setRenameDialogOpen(false);
    };

    const downloadModel = (modelName: string) => {
        window.open(`${tminingUrl}${urls.download(modelName)}`);
        alertTextMethod("Downloading model " + modelName + " is started", "success");
    }

    const downloadSelectedModels = () => {
        try {
            selected.forEach(modelName => {
                downloadModel(modelName);
            });
            alertTextMethod("Downloading selected models is ended", "success")
        } catch (error) {
            alertTextMethod("Failed to download selected models: " + error, "error")
        }
    };

    const copyToClipboard = (text: string) => {
        navigator.clipboard.writeText(text).then(() => alertTextMethod("Copied to clipboard", "success")).catch(e => alertTextMethod("Failed to copy to clipboard: " + e, "error"));
    }

    const handleRequestSort = (_event: React.MouseEvent<unknown>, property: keyof typeof models[0]) => {
        const isAsc = orderBy === property && order === 'asc';
        setOrder(isAsc ? 'desc' : 'asc');
        setOrderBy(property);
    };

    function stableSort<T>(array: readonly T[], comparator: (a: T, b: T) => number) {
      const stabilizedThis = array.map((el, index) => [el, index] as [T, number]);
      stabilizedThis.sort((a, b) => {
        const order = comparator(a[0], b[0]);
        if (order !== 0) {
          return order;
        }
        return a[1] - b[1];
      });
      return stabilizedThis.map((el) => el[0]);
    }

    type Order = 'asc' | 'desc';

    function getComparator<Key extends keyof any>(
      order: Order,
      orderBy: Key,
    ): (
      a: { [key in Key]: number | string },
      b: { [key in Key]: number | string },
    ) => number {
      return order === 'desc'
        ? (a, b) => descendingComparator(a, b, orderBy)
        : (a, b) => -descendingComparator(a, b, orderBy);
    }

    function descendingComparator<T>(a: T, b: T, orderBy: keyof T) {
      if (b[orderBy] < a[orderBy]) {
        return -1;
      }
      if (b[orderBy] > a[orderBy]) {
        return 1;
      }
      return 0;
    }

    const handleSelectAllClick = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.checked) {
            const newSelecteds = models.map((n) => n.uuid);
            setSelected(newSelecteds);
            return;
        }
        setSelected([]);
    };

    const handleClick = (_event: React.MouseEvent<unknown>, name: string) => {
        const selectedIndex = selected.indexOf(name);
        let newSelected: Array<any> = [];

        if (selectedIndex === -1) {
            newSelected = newSelected.concat(selected, name);
        } else if (selectedIndex === 0) {
            newSelected = newSelected.concat(selected.slice(1));
        } else if (selectedIndex === selected.length - 1) {
            newSelected = newSelected.concat(selected.slice(0, -1));
        } else if (selectedIndex > 0) {
            newSelected = newSelected.concat(
                selected.slice(0, selectedIndex),
                selected.slice(selectedIndex + 1),
            );
        }

        setSelected(newSelected);
    };

    const handleChangePage = (_event: unknown, newPage: number) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };

    const isSelected = (name: string) => selected.indexOf(name) !== -1;

    return (
        <div>
            <Backdrop
                sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
                open={loading}
            >
                <CircularProgress color="inherit" />
            </Backdrop>
            {alertOpen && (
                <Alert severity={severity} onClose={() => setAlertOpen(false)}>
                    {alertText}
                </Alert>
            )}
            <ActionPanel onDownload={downloadSelectedModels} onDelete={deleteSelectedModels} onUpload={handleUploadClick} selected={selected.length}/>
            {models.length === 0 ? (
                <Alert severity="info" action={
                    <Button color="inherit" size="small" onClick={() => navigate('/#training')}>
                        Go to Training
                    </Button>
                }>
                    No models found. Please use Train option to create a new model.
                </Alert>
            ) : (
                <Paper>
                    <TableContainer>
                        <Table
                            sx={{ minWidth: 750 }}
                            aria-labelledby="tableTitle"
                            size='medium'
                        >
                            <TableHead>
                                <TableRow>
                                    <TableCell padding="checkbox">
                                        <Checkbox
                                            color="primary"
                                            indeterminate={selected.length > 0 && selected.length < models.length}
                                            checked={models.length > 0 && selected.length === models.length}
                                            onChange={handleSelectAllClick}
                                            inputProps={{
                                                'aria-label': 'select all models',
                                            }}
                                        />
                                    </TableCell>
                                    {['name', 'uuid', 'shared', ''].map((headCell) => (
                                        <TableCell
                                            key={headCell}
                                            align='left'
                                            padding='normal'
                                            sortDirection={orderBy === headCell ? order : false}
                                        >
                                            <TableSortLabel
                                                active={orderBy === headCell}
                                                direction={orderBy === headCell ? order : 'asc'}
                                                onClick={(event) => handleRequestSort(event, headCell)}
                                            >
                                                {headCell}
                                                {orderBy === headCell ? (
                                                    <Box component="span" sx={visuallyHidden}>
                                                        {order === 'desc' ? 'sorted descending' : 'sorted ascending'}
                                                    </Box>
                                                ) : null}
                                            </TableSortLabel>
                                        </TableCell>
                                    ))}
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {stableSort(models, getComparator(order, orderBy))
                                    .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                                    .map((model: typeof models[0], index: number) => {
                                        const isItemSelected = isSelected(model.uuid);
                                        const labelId = `enhanced-table-checkbox-${index}`;

                                        return (
                                            <TableRow
                                                hover
                                                onClick={(event) => handleClick(event, model.uuid)}
                                                role="checkbox"
                                                aria-checked={isItemSelected}
                                                tabIndex={-1}
                                                key={model.uuid}
                                                selected={isItemSelected}
                                            >
                                                <TableCell padding="checkbox">
                                                    <Checkbox
                                                        color="primary"
                                                        checked={isItemSelected}
                                                        inputProps={{
                                                            'aria-labelledby': labelId,
                                                        }}
                                                    />
                                                </TableCell>
                                                <TableCell
                                                    component="th" id={labelId} scope="row" padding="none"
                                                >
                                                    {model.name}
                                                </TableCell>
                                                <TableCell>{model.uuid}</TableCell>
                                                <TableCell>{model.shared ? <LockOpenIcon /> : <LockIcon />}</TableCell>
                                                <TableCell>
                                                    <IconButton onClick={(event) => {
                                                    event.stopPropagation();
                                                    copyToClipboard(model.uuid);
                                                }}>
                                                    <FileCopyOutlinedIcon />
                                                </IconButton>
                                                <IconButton onClick={(event) => {
                                                    event.stopPropagation();
                                                    downloadModel(model.uuid);
                                                }}>
                                                    <GetAppIcon />
                                                </IconButton>
                                                <IconButton onClick={(event) => {
                                                    event.stopPropagation();
                                                    handleRenameClick(model.uuid, model.name, model.shared);
                                                }}>
                                                    <EditIcon />
                                                </IconButton>
                                                <IconButton onClick={(event) => {
                                                    event.stopPropagation();
                                                    deleteModel(model.uuid);
                                                }}>
                                                    <DeleteIcon />
                                                </IconButton>
                                                </TableCell>
                                            </TableRow>
                                        );
                                    })}
                            </TableBody>
                            <TableFooter>
                                <TableRow>
                                    <TablePagination
                                        rowsPerPageOptions={[5, 10, 25]}
                                        // component="div"
                                        count={models.length}
                                        rowsPerPage={rowsPerPage}
                                        page={page}
                                        onPageChange={handleChangePage}
                                        onRowsPerPageChange={handleChangeRowsPerPage}
                                    />
                                </TableRow>
                            </TableFooter>
                        </Table>
                    </TableContainer>
                </Paper>
                )}
            <Dialog open={renameDialogOpen} onClose={handleRenameDialogClose}>
                        <DialogTitle>Edit Model</DialogTitle>
                        <DialogContent>
                            <DialogContentText>
                            </DialogContentText>
                            <TextField
                                autoFocus
                                margin="dense"
                                label="New Model Name"
                                type="text"
                                fullWidth
                                defaultValue={currentModelName}
                                onChange={(event) => setNewModelName(event.target.value)}
                            />
                            <FormControlLabel
                                control={<Switch checked={currentShared} onChange={(event) => setCurrentShared(event.target.checked)} />}
                                label="Shared"
                            />
                        </DialogContent>
                        <DialogActions>
                            <Button onClick={handleRenameDialogClose}>Cancel</Button>
                            <Button onClick={handleRenameConfirm}>Edit</Button>
                        </DialogActions>
                    </Dialog>
                    <Dialog open={deleteDialogOpen} onClose={handleDeleteDialogClose}>
                        <DialogTitle>Delete Selected Models</DialogTitle>
                        <DialogContent>
                            <DialogContentText>
                                Are you sure you want to delete the selected models?
                            </DialogContentText>
                        </DialogContent>
                        <DialogActions>
                            <Button onClick={handleDeleteDialogClose}>Cancel</Button>
                            <Button onClick={handleDeleteConfirm}>Delete</Button>
                        </DialogActions>
                    </Dialog>
                    <Dialog open={uploadDialogOpen} onClose={handleUploadDialogClose}>
                      <DialogTitle>Upload Model</DialogTitle>
                      <DialogContent>
                        <form onSubmit={handleSubmit(onSubmit)}>
                          <UploadFileInput
                            fileName={"model"}
                            register={register}
                            registerAs={"model"}
                            fileError={errors.model}
                          />
                          <FormControlLabel
                            control={<Switch checked={shared} onChange={handleSharedChange} />}
                            label="Shared"
                          />
                        </form>
                      </DialogContent>
                      <DialogActions>
                        <Button onClick={handleUploadDialogClose}>Cancel</Button>
                        <Button onClick={handleSubmit(onSubmit)}>Upload</Button>
                      </DialogActions>
                    </Dialog>
        </div>
    )
}

export {ModelsPage}