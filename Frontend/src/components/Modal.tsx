import {
  Image,
  ModalDivider,
  ModuleBody,
  ModuleChild,
  ModuleChildTitle,
  ModuleChildValue,
  ModuleContainer,
  ModuleHeader,
} from '../styled/Modal.style';
import { Modal, Slide } from '@mui/material';
import close from '../assets/close.svg';
import ModalStore from '../stores/Modal.store';
import { observer } from 'mobx-react-lite';
import { useEffect } from 'react';
import API from '../utils/API';
const ModalComponent = observer(() => {
  useEffect(() => {
    API.getModalData().then((res) => {
      ModalStore.setModuleData('warnings', res['result']['warnings']);
      ModalStore.setModuleData('errors', res['result']['errors']);
      ModalStore.setModuleData('mainError', res['result']['mainError']);
      ModalStore.setModuleData(
        'possibleReason',
        res['result']['possibleReason']
      );
      ModalStore.setModuleData('possiblePatch', res['result']['possiblePatch']);
            ModalStore.setModuleData('badLines', res['badLines']);
    });
  }, []);
  return (
    <Modal
      style={{ backdropFilter: 'blur(5px)' }}
      closeAfterTransition
      slotProps={{
        backdrop: {
          timeout: 500,
        },
      }}
      open={ModalStore.getOpen()}
      onClose={() => {
        ModalStore.setOpen(!ModalStore.getOpen());
      }}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Slide
        direction="up"
        in={ModalStore.getOpen()}
        timeout={{ enter: 500, exit: 500 }}
      >
        <ModuleContainer>
          <ModuleHeader>
            <Image src={close} onClick={() => ModalStore.setOpen(false)} />
          </ModuleHeader>
          <ModuleBody>
            <ModuleChild>
              <ModuleChildTitle>Name</ModuleChildTitle>
              <ModuleChildValue>
                {ModalStore.getModuleData().name}
              </ModuleChildValue>
            </ModuleChild>
            <ModuleChild>
              <ModuleChildTitle>Version</ModuleChildTitle>
              <ModuleChildValue>
                {ModalStore.getModuleData().version}
              </ModuleChildValue>
            </ModuleChild>
            <ModalDivider />
            <ModuleChild>
              <ModuleChildTitle>Warnings</ModuleChildTitle>
              <ModuleChildValue>
                {ModalStore.getModuleData().warnings}
              </ModuleChildValue>
            </ModuleChild>
            <ModuleChild>
              <ModuleChildTitle>Errors</ModuleChildTitle>
              <ModuleChildValue>
                {ModalStore.getModuleData().errors}
              </ModuleChildValue>
            </ModuleChild>
            <ModuleChild>
              <ModuleChildTitle>Main error</ModuleChildTitle>
              <ModuleChildValue>
                {ModalStore.getModuleData().mainError}
              </ModuleChildValue>
            </ModuleChild>
            <ModuleChild>
              <ModuleChildTitle>Possible reason</ModuleChildTitle>
              <ModuleChildValue>
                {ModalStore.getModuleData().possibleReason}
              </ModuleChildValue>
            </ModuleChild>
            <ModuleChild>
              <ModuleChildTitle>Possible patch</ModuleChildTitle>
              <ModuleChildValue>
                {ModalStore.getModuleData().possiblePatch}
              </ModuleChildValue>
            </ModuleChild>
              <ModuleChild>
              <ModuleChildTitle>Bad lines</ModuleChildTitle>
              <ModuleChildValue>
                {ModalStore.getModuleData()?.badLines?ModalStore.getModuleData()?.badLines[0]:""}
              </ModuleChildValue>
              <ModuleChildValue>
                  {ModalStore.getModuleData()?.badLines?ModalStore.getModuleData()?.badLines[1]:""}
              </ModuleChildValue>
              <ModuleChildValue>
                  {ModalStore.getModuleData()?.badLines?ModalStore.getModuleData()?.badLines[2]:""}
              </ModuleChildValue>
              <ModuleChildValue>
               {ModalStore.getModuleData()?.badLines?ModalStore.getModuleData()?.badLines[3]:""}
              </ModuleChildValue>
              <ModuleChildValue>
                {ModalStore.getModuleData()?.badLines?ModalStore.getModuleData()?.badLines[4]:""}
              </ModuleChildValue>
            </ModuleChild>
          </ModuleBody>
        </ModuleContainer>
      </Slide>
    </Modal>
  );
});

export default ModalComponent;
