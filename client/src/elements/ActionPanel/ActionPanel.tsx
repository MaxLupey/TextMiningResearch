import React from 'react';
import {Button} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import DownloadIcon from '@mui/icons-material/Download';
import css from './ActionPanel.module.css';
import UploadIcon from '@mui/icons-material/Upload';
import {ActionPanelProps} from '../../interfaces/action.panel.interface'

const ActionPanel: React.FC<ActionPanelProps> = ({ onDownload, onDelete, onUpload, selected }) => {

    const disabled = selected == 0;


  return (
    <div className={css.panel}>
      <Button variant="contained" color="primary" onClick={onDownload} disabled={disabled}>
        <DownloadIcon />
      </Button>
      <Button variant="contained" color="primary" onClick={onDelete} disabled={disabled}>
        <DeleteIcon />
      </Button>
        <Button variant="contained" color="primary" onClick={onUpload}>
            <UploadIcon />
        </Button>
    </div>
  );
};

export default ActionPanel;