import React, { useState } from 'react';
import type { FC } from 'react';
import useDrivePicker from 'react-google-drive-picker';
import {
  Box,
  Button,
} from '@mantine/core';

const GooglePicker: FC = () => {
  const [openPicker] = useDrivePicker();

  const handleOpenPicker = () => {
    gapi.load('client:auth2', () => {
      gapi.client
        .init({
          apiKey: process.env.NEXT_PUBLIC_GOOGLE_API_KEY,
        })
        .then(() => {
          let tokenInfo = gapi.auth.getToken();
          const pickerConfig: any = {
            clientId: process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID,
            developerKey: process.env.NEXT_PUBLIC_GOOGLE_API_KEY,
            viewId: 'SPREADSHEETS',
            viewMimeTypes: 'application/vnd.google-apps.spreadsheet',
            token: tokenInfo ? tokenInfo.access_token : null,
            showUploadView: true,
            showUploadFolders: true,
            supportDrives: true,
            multiselect: true,
            callbackFunction: async (data) => {
              const elements = Array.from(
                document.getElementsByClassName(
                  'picker-dialog'
                ) as HTMLCollectionOf<HTMLElement>
              );
              for (let i = 0; i < elements.length; i++) {
                elements[i].style.zIndex = '2000';
              }
              if (data.action === 'picked' && data?.docs?.length) {
                //Add your desired workflow when choosing a file from the Google Picker popup
                //In this below code, I'm attempting to get the file's information.
                console.log({ data })


                for(const doc of data.docs){
                  const fileId = doc.id
                  if(fileId){
                    const filename = doc.name;
                    //GET https://sheets.googleapis.com/v4/spreadsheets/ + sheetid using fetch
                    const response = await fetch(`https://sheets.googleapis.com/v4/spreadsheets/${fileId}`, {
                      headers: {
                        Authorization: `Bearer ${tokenInfo.access_token}`,
                      },
                    });
                    const sheetData = await response.json();
                    const sheets = sheetData.sheets;
                    for(const sheet of sheets) {
                      const id = sheet.sheetId;
                      const url = 'https://docs.google.com/spreadsheets/d/' + fileId + '/gviz/tq?tqx=out:csv&sheet=' + id
                      //get csv file
                      const res = await fetch(url, {
                        headers: {
                          Authorization: `Bearer ${tokenInfo.access_token}`,
                        },
                      });
                      const csv = await res.text();
                      console.log({ csv })
                    }

                  }
                }


              }
            },
          };
          openPicker(pickerConfig);
        });
    });
  };

  return (
    <Box>
      <Button
        onClick={() => handleOpenPicker()}
        color="primary"
        variant="outlined"
      >
        Open Google Picker
      </Button>
    </Box>
  );
};

export default GooglePicker;
